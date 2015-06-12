from brian2 import *
prefs.codegen.target = 'numpy'

class NeuronNetwork:
    def __init__(self, N, threshold_voltage=30*mV):
        self.G = NeuronGroup(N, model='''
            a : 1
            b : 1
            c : 1
            d : 1
            k : 1
            dv/dt = (0.04*(v/mV)**2 + 5*v/mV + 140 - u/mV + I/mV)*mV / ms : volt
            du/dt = a*(b*v-u) / ms: volt
            dI/dt = -log(2)*I/ms: volt 
        ''', threshold='v >= %f * mV' % (threshold_voltage/mV), reset='''
            v = c*mV
            u = u + d*mV
        ''')
        self.G.I = 0
        self.G.v = -65 * mV

        self.S = Synapses(self.G, self.G, model = '''w:volt''', pre='''I += k_pre*w''')

    def assign_RSneurons(self, indices):
        for i in indices:
            self.G.a[i] = 0.02
            self.G.b[i] = 0.2
            self.G.c[i] = -65
            self.G.d[i] = 8
            self.G.k[i] = 1

    def assign_FSneurons(self, indices):
        for i in indices:
            self.G.a[i] = 0.1
            self.G.b[i] = 0.2
            self.G.c[i] = -65
            self.G.d[i] = 2
            self.G.k[i] = -1
            #self.G.a[i] = 0.02
            #self.G.b[i] = 0.2
            #self.G.c[i] = -65
            #self.G.d[i] = 8
            #self.G.k[i] = -1
    
    def establish_connections(self, *args, **kargs):
        self.S.connect(*args, **kargs)

NE = 800
NI = 200
N = 1000

net = NeuronNetwork(N)
net.assign_RSneurons(range(NE))
net.assign_FSneurons(range(NE,N))

net.establish_connections('i!=j', p=0.1)
net.S.w = 5*mV
net.S.delay = 'rand() * 20*ms'


#M = StateMonitor(net.G, ('v','u','I'), record=[0, 1, 2, 3])
mon = SpikeMonitor(net.G)
monp = PopulationRateMonitor(net.G)



@network_operation(dt = 1*ms)
def update_active(t):
    net.G.I[randint(0, N)] = 30 * mV

m = Network(collect())
m.add(net.G)
m.add(net.S)
m.add(update_active)
m.run(1*second, report='text')

#subplot(2, 2, 1)
#plot(M.t/ms, M.v[0]/mV, label='v')
#subplot(2, 2, 2)
#plot(M.t/ms, M.v[1]/mV, label='v')
#subplot(2, 2, 3)
#plot(M.t/ms, M.v[2]/mV, label='v')
#subplot(2, 2, 4)
#plot(M.t/ms, M.v[3]/mV, label='v')

subplot(2,1,1)
plot(mon.t / ms, mon.i, ',')
subplot(2,1,2)
plot(monp.t / ms, monp.rate/Hz)
#subplot(2,2,1)
#plot(mon.t / ms, sum(mon.i), ',')
show()

