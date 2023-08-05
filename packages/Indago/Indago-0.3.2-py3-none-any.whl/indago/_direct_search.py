#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._optimizer import Optimizer, CandidateState 
import numpy as np

class NelderMead(Optimizer):
    """Squirrel Search Algorithm class"""

    def __init__(self):
        """Initialization"""
        Optimizer.__init__(self)

        self.X = None
        self.X0 = None
        self.variant = 'Vanilla'
        self.params = {}
        self.params['init_step'] = 0.4
        self.params['alpha'] = 1.0
        self.params['gamma'] = 2.0
        self.params['rho'] = 0.5
        self.params['sigma'] = 0.5
        self.iterations = 100


    def _check_params(self):

        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.variant == 'Vanilla':
            mandatory_params = ''.split()
            optional_params = 'init_step alpha gamma rho sigma'.split()

        for param in mandatory_params:
            # if param not in defined_params:
            #    print('Error: Missing parameter (%s)' % param)
            assert param in defined_params, f'Error: Missing parameter {param}'

        for param in defined_params:
            if param not in mandatory_params and param not in optional_params:
                self.log(f'Warning: Excessive parameter {param}')

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)

    def _init_method(self):
        # Bounds for position and velocity
        self.lb = np.array(self.lb)
        self.ub = np.array(self.ub)

        # Generate set of points
        self.cS = np.array([CandidateState(self) for _ in range(self.dimensions + 1)], \
                            dtype=CandidateState)

        # Generate initial positions
        #self.cS[0].X = 0.5 * (self.lb + self.ub)
        self.cS[0].X = np.random.uniform(self.lb, self.ub)
        if self.X0 is not None:
                if np.shape(self.X0)[0] > 0:
                    self.cS[0].X = self.X0[0]
        self.collective_evaluation(self.cS[:1])
        # self.log(self.cS[0].X)
        # self.cS[0].evaluate()
        # print(self.cS[0].X)

        for p in range(1, self.dimensions + 1):

            # Random position
            dx = np.zeros([self.dimensions])
            dx[p - 1] = self.params['init_step']
            self.cS[p].X = self.cS[0].X + dx * (self.ub - self.lb)
            self.cS[p].X = np.clip(self.cS[p].X, self.lb, self.ub)

            # Using specified particles initial positions
            if self.X0 is not None:
                if p < np.shape(self.X0)[0]:
                    self.cS[p].X = self.X0[p]

            # self.log(self.cS[p].X)
        # Evaluate
        self.collective_evaluation(self.cS)

    def _run(self):
        self._check_params()
        self._init_method()

        for self.it in range(self.iterations):
            self.cS = np.sort(self.cS)
            # print(self.it, np.min(self.cS).f)
            #print(i, self.cS[0].f, self.cS[-1].f)

            self._progress_log()

            # Check stopping conditions
            if self._stopping_criteria():
                break

            # Center
            X0 = np.zeros(self.dimensions)
            for p in range(self.dimensions):
                X0 += self.cS[p].X
            X0 /= self.dimensions

            dX = X0 - self.cS[-1].X

            # Reflection
            Xr = X0 + self.params['alpha'] * dX
            Xr = np.clip(Xr, self.lb, self.ub)
            cR = CandidateState(self)
            cR.X = Xr
            # cR.evaluate()
            self.collective_evaluation([cR])

            if self.cS[0] <= cR <= self.cS[-2]:
                self.cS[-1] = cR.copy()
                #print('Rf')
                continue


            # Expansion
            if cR < self.cS[0]:
                Xe = X0 + self.params['gamma'] * dX
                Xe = np.clip(Xe, self.lb, self.ub)
                cE = CandidateState(self)
                cE.X = Xe
                # cE.evaluate()
                self.collective_evaluation([cE])

                if cE < cR:
                    self.cS[-1] = cE.copy()
                    #print('Ex')
                    continue
                else:
                    self.cS[-1] = cR.copy()
                    #print('Rf')
                    continue


            # Contraction
            if cR < self.cS[-1]:

                Xc = X0 + self.params['rho'] * dX
                Xc = np.clip(Xc, self.lb, self.ub)
                cC = CandidateState(self)
                cC.X = Xc
                # cC.evaluate()
                self.collective_evaluation([cC])

                if cC < self.cS[-1]:
                    self.cS[-1] = cC.copy()
                    #print('Ct')
                    continue

            else:

                Xc = X0 - self.params['rho'] * dX
                Xc = np.clip(Xc, self.lb, self.ub)
                cC = CandidateState(self)
                cC.X = Xc
                # cC.evaluate()
                self.collective_evaluation([cC])

                if cC < self.cS[-1]:
                    self.cS[-1] = cC.copy()
                    #print('Ct')
                    continue

            # Reduction
            for p in range(1, self.dimensions + 1):
                self.cS[p].X = self.cS[0].X + self.params['sigma'] * (self.cS[p].X - self.cS[0].X)
                # self.cS[p].evaluate()
            self.collective_evaluation(self.cS[1:])


        return self.best


class MSGS(Optimizer):
    """Multi Scale Grid Search class"""

    def __init__(self):
        """Initialization"""
        Optimizer.__init__(self)
        self.X0 = None
        self.X = None
        self.variant = 'Vanilla'
        self.params = {}
        self.params['n'] = 10
        self.params['xtol'] = 1e-4
        self.iterations = 100

    def _check_params(self):

        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []
        
        if 'n' in self.params:
            self.params['n'] = int(self.params['n'])

        if self.variant == 'Vanilla':
            mandatory_params = ''.split()
            optional_params = 'n xtol'.split()

        for param in mandatory_params:
            # if param not in defined_params:
            #    print('Error: Missing parameter (%s)' % param)
            assert param in defined_params, f'Error: Missing parameter {param}'

        for param in defined_params:
            if param not in mandatory_params and param not in optional_params:
                self.log(f'Warning: Excessive parameter {param}')

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)


    def _init_method(self):
        # Bounds for position and velocity
        self.lb = np.array(self.lb)
        self.ub = np.array(self.ub)

        self._n = self.params['n']
        self._I = np.arange(-self._n, self._n + 1)

        self._x = CandidateState(self)
        if self.X0 is not None:
            self._x.X = self.X0[0, :]
        else:
            self._x.X = np.random.uniform(self.lb, self.ub)

        self._center = 0.5 * (self.lb + self.ub)
        self._reinit_grid(self._center, 1, 'Initial grid')
        self._x = self._y_to_x(self._y)

        self.collective_evaluation([self._x])
        self._H.append(list(self._y))
        self.log(f'Initial point: {self._x.X}')

    def _reinit_grid(self, center, scale, grid_action):
        # self.log(f'Init grid @{self.best.X if self.best else "None"} x{self._scale}')
        dx = (self.ub - self.lb) / (2 * self._n * scale)

        new_center = center.copy()
        for i in range(self.dimensions):
            xi = new_center[i] + self._I * dx[i]
            # self.log(f'{xi=}')
            dil = int(np.sum(xi < self.lb[i]))
            new_center[i] += dx[i] * dil
            diu = int(np.sum(xi > self.ub[i]))
            new_center[i] -= dx[i] * diu
            # if dil > 0 or diu > 0:
            #     pass
            #     # Bounds_reached

        self._X_map = [new_center[i] + self._I * dx[i] for i in range(self.dimensions)]
        self._y = self._x_to_y(self._x)
        self._H = [list(self._y)]

        self.log(f'Grid reinitialization {scale=}, {grid_action=}')
        if np.all(np.isclose(self._center, new_center, (self.ub - self.lb) * self.params['xtol'] * 1e-3)):
            # Center unchanged
            self.log(f'c: {self._center}')
            self.log(f'c: {new_center}')
            return False
        else:
            # Center changed
            return True

    def _x_to_y(self, x):
        y = np.zeros(self.dimensions, dtype=int)
        for i in range(self.dimensions):
            y[i] = np.argmin(np.abs(x.X[i] - self._X_map[i])) - self._n
        return y

    def _y_to_x(self, y):
        x = CandidateState(self)
        for i in range(self.dimensions):
            x.X[i] = self._X_map[i][y[i] + self._n]
        return x

    def _find_dir(self, y, dy=None):

        # self.log(f'{y=}')
        # self.log(f'{self._x.X=}')
        new_dy = np.zeros_like(y, dtype=int)
        eval_map = np.full(self.dimensions * 2, -1, dtype=int)
        C = np.array([], dtype=CandidateState)
        cnt = 0

        for i in range(self.dimensions):
            _dy = np.zeros(self.dimensions, dtype=int)
            _dy[i] = -1
            yn = y + _dy
            _dy[i] = 1
            yp = y + _dy

            calc_n = True
            calc_p = True
            if dy is not None:
                if dy[i] == 1:
                    calc_p = False
                if dy[i] == -1:
                    calc_n = False

            if np.abs(yn[i]) <= self._n and calc_n:
                C = np.append(C, np.array([self._y_to_x(yn)]))
                eval_map[2 * i + 0] = cnt
                cnt += 1

            if np.abs(yp[i]) <= self._n and calc_p:
                C = np.append(C, np.array([self._y_to_x(yp)]))
                eval_map[2 * i + 1] = cnt
                cnt += 1

        self.collective_evaluation(C)

        for i in range(self.dimensions):
            c0 = self._x

            if eval_map[2 * 1 + 0] >= 0:
                cn = C[eval_map[2 * i + 0]]
            else:
                cn = None

            if eval_map[2 * 1 + 1] >= 0:
                cp = C[eval_map[2 * i + 1]]
            else:
                cp = None

            if cp and cn:
                new_dy[i] = np.argmin([cn, c0, cp]) - 1
            elif cp:
                new_dy[i] = np.argmin([c0, cp])
            elif cn:
                new_dy[i] = np.argmin([cn, c0]) - 1
            else:
                new_dy[i] = 0

        # self.log(f'{new_dy=}')
        return new_dy

    def _run(self):
        self._check_params()
        self._init_method()

        k, k_max = 0, 2
        d = self.dimensions

        scale = 1
        grid_action = 'none'
        action = 'find_dir_3p'
        shift_count = 0

        for self.it in range(self.iterations):

            # self.log(f'{grid_action=}, {action=}')
            self._update_history()  # Adding history record allows iterations without evaluation

            if grid_action == 'shift':
                if shift_count >= 2 and scale >= 2:
                    scale = int(scale / 2)
                    shift_count = 0
                    self.log('scale_down (3rd consecutive shift)')

                if self._reinit_grid(self._x.X, scale, grid_action):
                    # Genter is changed
                    #action = 'move'
                    grid_action = 'none'
                    shift_count += 1
                    self.log(f'shift ({shift_count=})')
                else:
                    scale = scale * 8
                    self._reinit_grid(self.best.X, scale, 'scale_up (shift failed)')
                    action = 'find_dir_3p'
                    grid_action = 'none'

            elif grid_action == 'scale_up':
                scale *= 8
                self._reinit_grid(self._x.X, scale, grid_action)
                action = 'find_dir_3p'
                grid_action = 'none'
                shift_count = 0

            elif grid_action == 'scale_down':
                if scale >= 2:
                    scale /= 2
                self._reinit_grid(self._x.X, scale)
                action = 'find_dir_3p'
                grid_action = 'none'
                shift_count = 0

            elif grid_action == 'none':
                pass
            else:
                assert False, f'Unknown {grid_action=}'


            if action == 'find_dir_3p':
                # Finding a new direction based on the full gradient calculation
                dy = self._find_dir(self._y)
                action = 'check_dir'

            elif action == 'find_dir_2p':
                # Finding a new direction based on one-side gradient calculation
                dy = self._find_dir(self._y, dy)
                action = 'check_dir'
                k += 1

            elif action == 'check_dir':
                # Moving in dy direction
                new_y = self._y + dy
                # Trimming bounds
                for i in range(d):
                    new_y[new_y < -self._n] = - self._n
                    new_y[new_y > self._n] = self._n
                dy = new_y - self._y

                if np.sum(np.abs(dy)) == 0:
                    # None of x_next's neighbouring points are better
                    if self._x == self.best:
                        # x_next is the best, hence convergence is finished
                        action = 'converged'
                    else:
                        action = 'move_to_best'
                else:
                    action = 'move'
                    bound_y = np.abs(self._y) == self._n
                    if np.any(bound_y):
                        new_x = self._y_to_x(self._y).X

                        bound_x = np.logical_or(np.isclose(new_x, self.lb),
                                                np.isclose(new_x, self.ub))

                        if np.sum(bound_y) == np.sum(bound_x):
                            # Reached lb/ub bounds, no rescaling needed
                            pass
                        else:
                            # action = 'none'
                            grid_action = 'shift'

            elif action == 'move_to_best':
                # Switching to the best point
                self._y = self._x_to_y(self.best)
                self._x = self.best.copy()
                action = 'find_dir_3p'
                k = 0

            elif action == 'move':
                # Moving in dy direction
                self._y = self._y + dy

                if list(self._y) in self._H:
                    action = 'move_to_best'
                else:
                    # Calculate x_next
                    x_last = self._x.copy()
                    self._x = self._y_to_x(self._y)
                    # Evaluate x_next
                    self.collective_evaluation([self._x])
                    self._H.append(list(self._y))

                # Set finding new direction if there is no improvement in new point
                if self._x <= x_last:
                    action = 'check_dir'
                elif k < k_max:
                    action = 'find_dir_2p'
                else:
                    action = 'move_to_best'

            elif action == 'converged':
                self._x = self.best
                rel_err = 1 / (2 * self._n * scale)
                # print(f'{dx=}')
                if np.all(rel_err < self.params['xtol']):
                    self.log(f'Relative precision reached for all optimization variables.')
                    break
                grid_action = 'scale_up'

            else:
                assert False, f'Unknown action {action=}'

            self._progress_log()

            # Check stopping conditions
            if self._stopping_criteria():
                self.log('Stop')
                break

        return self.best

