import os
import torch
from botorch.acquisition.multi_objective.monte_carlo import qExpectedHypervolumeImprovement, qNoisyExpectedHypervolumeImprovement
from botorch.optim.optimize import optimize_acqf
from botorch.models.gp_regression import HeteroskedasticSingleTaskGP, FixedNoiseGP, SingleTaskGP
from botorch.models.model_list_gp_regression import ModelListGP
from botorch.models.transforms.outcome import Standardize
from gpytorch.mlls.sum_marginal_log_likelihood import SumMarginalLogLikelihood
from botorch.exceptions import BadInitialCandidatesWarning
from botorch.utils.multi_objective.box_decompositions.dominated import DominatedPartitioning
from botorch.sampling.samplers import SobolQMCNormalSampler
from botorch.utils.transforms import unnormalize, normalize
from botorch.utils.sampling import draw_sobol_samples
import pandas as pd
import numpy as np
from .sample_space import generate_sample_space
import warnings
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pickle
import itertools
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae
import plotly.figure_factory as ff
import plotly.express as px
from math import ceil, floor

tkwargs = {
    "dtype": torch.double,
    #"device": torch.device("cuda" if torch.cuda.is_available() else "cpu"),
    "device": "cpu"
}
SMOKE_TEST = os.environ.get("SMOKE_TEST")


class Active_Learning_Loop:
    def __init__(self, filename, label_x, label_y, target, scaling = None):
        self.hypervolume = 0 
        self.label_x = label_x
        self.label_y = label_y
        if scaling is None:
            scaling = ['lin']*len(label_y)
        self.train_x, self.train_y, self.train_yvar, self.ref_point = self.read_data(filename, target, scale = scaling)
        self.model = None
        self.predictions_clean = pd.DataFrame()

    def run_Loop(self, rec_type = 'target'):
        warnings.filterwarnings('ignore', category=BadInitialCandidatesWarning)
        warnings.filterwarnings('ignore', category=RuntimeWarning)

        N_BATCH = 20 if not SMOKE_TEST else 10
        MC_SAMPLES = 512  if not SMOKE_TEST else 16

        hvs_qnehvi = []
        
        _, _ = self.initialize_model()
        
        # compute hypervolume
        bd = DominatedPartitioning(ref_point= self.ref_point, Y=self.train_y)
        volume = bd.compute_hypervolume().item()
        print('HYPERVOL', volume)
        #print(volume)
        self.hypervolume = volume
        hvs_qnehvi.append(volume)

        qnehvi_sampler = SobolQMCNormalSampler(num_samples=MC_SAMPLES)
            
            # optimize acquisition functions and get new observations

        if rec_type == 'target':
            new_x_qnehvi = self.optimize_qnehvi_and_get_observation(qnehvi_sampler)
            self.predictions_OG = self.get_prediction(new_x_qnehvi)
            self.predictions_clean = self.get_prediction(self.clean_predictions(new_x_qnehvi),  save = True)
        elif rec_type == 'uncertainty':
            x_new = self.uncertainty_selection()
            self.predictions_clean = self.get_prediction(x_new, save = True)
            self.predictions_OG = self.predictions_clean
        else:
            raise Exception("Incorrect Recommendation Type.")

        return self.predictions_OG, self.predictions_clean

    def clean_predictions(self, X):
        X = (X > 0.04).float()*X
        X = X / X.sum(dim=-1).unsqueeze(-1)
        X = torch.round(X, decimals = 3)
        return X

    def optimize_qnehvi_and_get_observation(self, sampler):
        """Optimizes the qEHVI acquisition function, and returns a new candidate and observation."""
        # partition non-dominated space into disjoint rectangles
        self.acq_func = qNoisyExpectedHypervolumeImprovement(
            model=self.model,
            ref_point=[-1.,-1.,-1.,-1.],#normalize(self.ref_point, self.y_bounds),  # use known reference point 
            X_baseline=self.train_x,
            prune_baseline=True,  # prune baseline points that have estimated zero probability of being Pareto optimal
            sampler=sampler,
        )
        # optimize
        
        
        samp_space = self.generate_initial_space().reshape(-1, 1, 3)
        print('init samples space', samp_space.shape)
        

        standard_bounds = torch.zeros(2, 3, **tkwargs)
        standard_bounds[1] = 1
        standard_bounds[0][1] = 0.07
        standard_bounds[0][0] = 0.07
        standard_bounds[0][2] = 0.07
        standard_bounds[1][-1] = 0.6

        
        candidates, _ = optimize_acqf(
            acq_function= self.acq_func,
            bounds=standard_bounds,
            q=5,
            num_restarts=5,
            raw_samples= 2000,  #used for intialization heuristic
            options= {"batch_limit": 5, "maxiter": 200, "disp":True},
            #batch_initial_conditions= samp_space,
            equality_constraints = [(torch.tensor([0,1,2], **{"dtype": torch.int64,"device": tkwargs["device"]}),torch.tensor(np.array([1,1,1]), **tkwargs), float(1.0))],
            #equality_constraints = [(torch.tensor([0,1,2], **{"dtype": torch.int64,"device": torch.device("cpu")}),torch.tensor(np.array([1,1,1]), **tkwargs), float(1.0))],
            sequential=False, #seq = True gives all points as tho predictions are independent
        )
        new_x = candidates.detach()
 
        return new_x

    def uncertainty_selection(self):
        X_pred = self.generate_initial_space(n = 60)
        raw_preds = self.get_prediction(X_pred, raw = True)
        overall_un = torch.sum(raw_preds.variance, axis = 1).item()
        chosen = X_pred[np.argmax(overall_un)]
        for i in range(4):
            score = torch.concat([torch.pow(X_pred - chosen[i],2).sum(axis = 1).reshape(-1,1) * -1 for i in range(chosen.shape[0])], axis = 1).sum(axis = 1)
            score = score/score.sum()
            new_aq = overall_un.add(score)
            chosen = torch.concat([chosen,X_pred[np.argmax(new_aq)]])
        
        return chosen
        

    def read_data(self, filename, targets, scale):
        if isinstance(filename, pd.DataFrame):
            data_frame = filename
        else:
            data_frame = pd.read_excel(filename)
        data_frame = data_frame.dropna(0)
        self.data_frame = data_frame
        print(data_frame)
        #data_frame = data_frame.loc[data_frame[['HEMA']].sum(axis=1) == 0,:]
        #data_frame = data_frame.loc[data_frame[['monomer 6']].sum(axis=1) == 0,:].fillna(0)
        self.initial_comps = data_frame[['Iteration'] + self.label_x]
        data_frame_x = data_frame[self.label_x]
        data_frame_y = data_frame[self.label_y]
        data_frame_yvar = data_frame[[p+'_stdev' for p in self.label_y]]
        # for p in self.label_y:
        #     data_frame_yvar[p+'_stdev'] = data_frame_yvar[p+'_stdev'] /data_frame[p]
        #print(data_frame_yvar)
        self.train_y_OG = torch.tensor(np.array(data_frame_y), **tkwargs)
        self.targets = {}
        self.scales = {}
        i = 0
        for c in data_frame_y.columns:
            if scale[i] == 'log10':
                print(c, data_frame_y[c].max() - data_frame_y[c].min())
                y_upper_sc = np.log10(data_frame_y[c] + data_frame_yvar[c+'_stdev'], dtype = np.float64)
                data_frame_y[c] = np.log10(data_frame_y[c])
                data_frame_yvar[c+'_stdev'] = y_upper_sc - data_frame_y[c]
                #data_frame_yvar[c+'_stdev'] = abs(data_frame_yvar[c+'_stdev'] /data_frame_y[c])
            self.scales[c] = scale[i]
            self.targets[c] = targets[i]
            i += 1
        train_x = torch.tensor(np.array(data_frame_x), **tkwargs)
        train_y = torch.tensor(np.array(data_frame_y), **tkwargs)

        train_yvar = torch.tensor(np.array(data_frame_yvar), **tkwargs)
        if 'min' in targets:
            min_prop = targets.index('min')
            train_y[:,min_prop] = -train_y[:,min_prop]
        ref_point = train_y.min(axis = 0)[0]
        print(train_y)
        print(ref_point)
        return train_x, train_y, train_yvar, ref_point

    def generate_initial_space(self, n = 20):
        s = [list(np.linspace(0, 1, n)), list(np.linspace(0, 1, n)), list(np.linspace(0, 1, n))]
        n = list(itertools.product(*s))
        out = torch.tensor([i for i in n if sum(i) == 1], **tkwargs)
        return out

    def initialize_model(self):
        # define models for objective and constraint
        #BOUNDS = torch.cat([torch.tensor([[0,0,0]], **tkwargs), torch.tensor([[1,1,1]], **tkwargs)])
        #train_x = normalize(self.train_x, BOUNDS)
        self.y_bounds= torch.stack([self.train_y.min(axis = 0)[0], self.train_y.max(axis = 0)[0]])

        self.train_y_norm = normalize(self.train_y, bounds = self.y_bounds)
        #self.train_yvar_norm = torch.pow(normalize(self.train_yvar + self.train_y.min(axis = 0)[0], bounds = self.y_bounds), 2)
        self.train_yvar_norm = torch.pow(normalize(self.train_yvar + self.train_y.min(axis = 0)[0], bounds = self.y_bounds), 2)
        
        #self.train_yvar_norm = self.train_yvar
        print('train vars',self.train_yvar_norm)
        
        
        models = []
        for i in range(self.train_y.shape[-1]):
            train_y = self.train_y_norm[..., i:i+1]
            train_yvar = self.train_yvar_norm[..., i:i+1]
            models.append(FixedNoiseGP(self.train_x, train_y, train_yvar, outcome_transform=Standardize(m=1)))
            #models.append(SingleTaskGP(self.train_x, train_y, outcome_transform=Standardize(m=1)))
        model = ModelListGP(*models)
        mll = SumMarginalLogLikelihood(model.likelihood, model)
        self.model = model
        return mll, model

    def get_prediction(self, X, save = False, raw = False):
        if type(X) == pd.core.frame.DataFrame:
            X = X[self.label_x].dropna(0)
            X = torch.tensor(X, **tkwargs)
        elif isinstance(X, list):
            X = torch.tensor(X, **tkwargs)
        
        out = self.model.posterior(X)
        if raw == True:
            return out
        if save:
            self.predictions_out = out.mean
        comps = pd.DataFrame(X.cpu().detach().numpy(), columns = self.label_x)
        props = pd.DataFrame(unnormalize(out.mean, self.y_bounds).cpu().detach().numpy(), columns = self.label_y)
        prop_var = pd.DataFrame((unnormalize(torch.sqrt(out.variance), self.y_bounds) - self.y_bounds[0]).cpu().detach().numpy(), columns = [p+'_stdev' for p in self.label_y])
        out = pd.concat([comps, props, prop_var], axis = 1)[self.label_x + sorted(self.label_y + [p+'_stdev' for p in self.label_y])]

        for k in self.label_y:
            if self.targets[k] == 'min':
                out[k] = -out[k]
            
            if self.scales[k] == 'log10':
                print(out[k+'_stdev'])
                yvar_unsc = np.power(10, out[k+'_stdev'] + out[k])
                out[k] = np.power(10, out[k])
                out[k + '_stdev'] = yvar_unsc - out[k]
        
        return out

    def calculate_hypervolume(self, data_type = 'original', norm = True):
        if norm: 
            rf = normalize(self.ref_point, self.y_bounds)
            y = self.train_y_norm
            if data_type == 'recs':
                y = torch.concat([y, self.predictions_out])
        else:
            rf = self.ref_point
            y = self.train_y
            if data_type == 'recs':
                y = torch.concat([y, unnormalize(self.predictions_out, self.y_bounds)])
        
        if data_type == 'original':
            bd = DominatedPartitioning(ref_point= rf, Y=y)
            volume = bd.compute_hypervolume().item()
            return volume
        
        if data_type == 'recs':
            bd = DominatedPartitioning(ref_point= rf, Y=y)
            volume = bd.compute_hypervolume().item()
            return volume
    
    def visualize_prop_space(self, data_type = 'original', props = [0,1], ref = None):

        if ref is None:
            ref = self.predictions_clean
        X = self.train_y_OG.cpu().detach().numpy()
        
        #pca = PCA(n_components=2)
        #pca = pca.fit(X)
        #X = pca.transform(X)
        plt.scatter(X[:,props[0]], X[:,props[1]], label = 'Original Data')
        plt.xlabel(self.label_y[props[0]])
        plt.ylabel(self.label_y[props[1]])
        if data_type == 'recs':
            X2 = np.array(ref[[self.label_y[props[0]], self.label_y[props[1]]]])
            #X2 = pca.transform(X2)
            #print(X2[:,0].shape)
            print(np.array(ref[self.label_y[props[0]]+'_stdev']))
            plt.errorbar(X2[:,0], X2[:,1], xerr = np.array(ref[self.label_y[props[0]]+'_stdev']), yerr = np.array(ref[self.label_y[props[1]]+'_stdev']), marker = 'o',ls='none',color = 'r', label = 'New Sample Predictions')
            #plt.errorbar(X2[:,0], X2[:,1] ,color = 'r', label = 'New Sample Predictions')

        plt.legend()
        plt.show()
    
    def ternary_visualization(self, add_data = None, save_path = ''):
        if add_data is None:
            add_data = self.predictions_clean
        add_data['Iteration'] = (max(self.initial_comps['Iteration']) + 1)
        #Show the compositions that we learned from
        # it_colors = {}

        # for it in self.initial_comps['Iteration'].unique():
        #     it_colors[it] = 
        
        df = pd.concat([self.initial_comps, add_data])
        df['Iteration'] = df['Iteration'].astype('str')
        df.to_excel(save_path + '/ternary_plot_data.xlsx')
        fig = px.scatter_ternary(df, a="IDA", b="IBOA", c="PEGDA", color = 'Iteration')
        fig.write_image(save_path + '/composition_visual.png')


        s = [list(np.linspace(0, 1, 50)), list(np.linspace(0, 1, 50)), list(np.linspace(0, 1, 50))]
        n = list(itertools.product(*s))
        X_pred = torch.tensor([i for i in n if sum(i) == 1], **tkwargs)
        raw_preds = self.get_prediction(X_pred, raw = True)
        print('Raw preds', raw_preds.mean)
        preds = self.get_prediction(X_pred)
        #preds = self.model.posterior(X_pred).mean.cpu().detach().numpy()
        x = X_pred.cpu().detach().numpy()
        coords = np.stack((x[:,0], x[:,1], x[:,2]))
        preds['Hypvol'] = 0
        preds['Hypvol_stdev'] = 0
        preds['qnehvi'] = 0
        preds['qnehvi_lin'] = 0

        
        for i in preds.index:
            bd = DominatedPartitioning(ref_point= raw_preds.mean.min(axis = 0)[0], Y = raw_preds.mean[i].reshape(1,-1))#Y=torch.stack([self.ref_point, raw_preds.mean[i]]).reshape(2,-1))#Y= normalize(raw_preds.mean[i], bounds = self.y_bounds).reshape(1,-1))
            preds.loc[i, 'qnehvi'] = self.acq_func(X_pred[i].reshape(1,1,3)).item()
            preds.loc[i,'qnehvi_lin'] = preds.loc[i, 'qnehvi']
            preds.loc[i, 'Hypvol'] = bd.compute_hypervolume().item()
            preds.loc[i, 'Hypvol_stdev'] = torch.sum(raw_preds.variance[i]).item()


        for prop in self.label_y + ['Hypvol', 'qnehvi', 'qnehvi_lin']:
            for app in ['', '_stdev']:
                colors = 'Jet' if app == '' else 'Greens'
                #fig = px.scatter_ternary(df, a="IDA", b="IBOA", c="PEGDA", color = 'Iteration')
                
                try:
                    if self.scales[prop] == 'log10':
                        preds[prop+app] = np.log10(preds[prop+app] + 0.0000000001)
                except:
                    print('prop not in scales dict')
                
                if prop == 'Hypvol':
                    print(preds[prop + app])

                if (prop == 'qnehvi' or prop == 'qnehvi_lin') and app == '_stdev':
                    continue

                try:
                    fig = ff.create_ternary_contour(coords,preds[prop + app], pole_labels=self.label_x, interp_mode='cartesian',ncontours=50,
                                            colorscale=colors,
                                            showscale=True,
                                            title= prop + app)
                except:
                    print(f'Error in calculation for {prop + app}')
                    continue
                
                    
                fig.update_ternaries(
                aaxis = dict(
                    tickmode = 'array',
                    ticklen = 10,
                    tickvals = [0.2, 0.4, 0.6, 0.8]#,
                    #ticktext = [r'0.2', r'0.4$', r'$0.6$', r'$0.8$']
                ),
                baxis = dict(
                    tickmode = 'array',
                    ticklen = 10,
                    tickvals = [0.2, 0.4, 0.6, 0.8]#,
                    #ticktext = [r'$0.2$', r'$0.4$', r'$0.6$', r'$0.8$']
                ),
                caxis = dict(
                    tickmode = 'array',
                    ticklen = 10,
                    tickvals = [0.2, 0.4, 0.6, 0.8]#,
                    #ticktext = [r'$0.2$', r'$0.4$', r'$0.6$', r'$0.8$']
                )
            )
                
                fig.update_layout(width=600, height=600)  
                fig.write_image(save_path + '/' + prop + app + '.png')

        self.ternary_predictions = preds.copy()
             
    def plot_parity(self, exp_data:pd.DataFrame(), save_path = None):
        compositions = torch.tensor(np.array(exp_data[['IDA', 'IBOA', 'PEGDA']]), **tkwargs)
        preds = self.get_prediction(compositions)
        error = {}
        for p in range(4):
            prop = self.label_y[p]

            if self.scales[prop] == 'log10':
                y_error = np.log10(np.array(preds.loc[:,prop]) + np.array(preds.loc[:,prop+'_stdev'])) - np.log10(np.array(preds.loc[:,prop]))
                x_error = np.log10(np.array(exp_data.loc[:,prop]) + np.array(exp_data.loc[:,prop + '_stdev'])) - np.log10(np.array(exp_data.loc[:,prop]))

                fig = plt.figure()
                ax = fig.add_subplot()
                for i in exp_data.index:
                    comp_str = ','.join(exp_data.loc[i, self.label_x].to_string(header=True).split('\n'))
                    plt.errorbar(np.log10(np.array(exp_data.loc[:, prop]))[i], np.log10(np.array(preds.loc[:,prop]))[i], xerr = x_error[i], yerr = y_error[i], marker =  '.', ls = 'none', label = comp_str)
                bounds = [floor(min(np.log10(np.array(preds.loc[:,prop])) - y_error)), ceil(max(np.log10(np.array(preds.loc[:,prop])) + y_error))]
                print('bounds', bounds)
                plt.plot(bounds, bounds, '--', color = 'k')
                plt.yticks(list(range(*bounds)))
                plt.xticks(list(range(*bounds)))
                ax.set_aspect('equal', adjustable='box')
                plt.title(prop + ' Predictions')
                plt.xlabel('log10 ' + prop + ' Experimental')
                plt.ylabel('log10 ' + prop + ' Predicted')
                print(prop, ' error: ', mae(np.log10(np.array(exp_data.loc[:, prop])), np.log10(np.array(preds.loc[:,prop]))))
                #print(error)
                error.update({prop: mae(np.log10(np.array(exp_data.loc[:, prop])), np.log10(np.array(preds.loc[:,prop])))})
                
                if p == 0:
                    plt.legend(bbox_to_anchor = (1, 1))
            elif self.scales[prop]== 'lin':
                fig = plt.figure()
                ax = fig.add_subplot()

                for i in exp_data.index:
                    comp_str = ','.join(exp_data.loc[i, self.label_x].to_string(header=True).split('\n'))
                    plt.errorbar(np.array(exp_data.loc[:, prop])[i], np.array(preds.loc[:,prop])[i], xerr = np.array(exp_data.loc[:,f'{prop}_stdev'])[i], yerr = np.array(preds.loc[:,f'{prop}_stdev'])[i], marker =  '.', ls = 'none',
                    label = comp_str)
                print(prop, ' error: ', mse(np.log10(np.array(exp_data.loc[:, prop])), np.log10(np.array(preds.loc[:,prop]))))
                error.update({prop: mse(np.array(exp_data.loc[:, prop]), np.array(preds.loc[:,prop]))})
                #print(error)
                bounds = [min(np.array(preds.loc[:,prop]) - y_error)-0.5, max(np.array(preds.loc[:,prop]) + y_error)+0.5]
                
                plt.plot(bounds, bounds, '--', color = 'k')
                ax.set_aspect('equal', adjustable='box')
                plt.title(prop + ' Predictions')
                plt.xlabel(prop + ' Experimental')
                plt.ylabel(prop + ' Predicted')
            
            if save_path:
                plt.savefig(save_path + f'/{prop}_parity.png')
            plt.close()
        return error
    
    def evaluation_metrics():
        pass

    def save(self, name = 'AL_loop'):
        fileObj = open(self, 'wb')
        pickle.dump(self,fileObj)
        fileObj.close()
        