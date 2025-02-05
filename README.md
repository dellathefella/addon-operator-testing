## A simple module example

Example of a sysctl tuner for nodes. Helm chart starts DaemonSet that periodically change sysctl parameters.

Useful parameters for production nodes can be found in [Brendan Gregg's Blog](http://www.brendangregg.com/blog/2017-12-31/reinvent-netflix-ec2-tuning.html).

> Note: this module will not revert sysctl parameters. Do not experiment on production nodes!


### local testing
```powershell
minikube start --nodes 2  --insecure-registry "10.0.0.0/24" -p multinode
minikube addons enable registry -p multinode
kubectl port-forward --namespace kube-system service/registry 5000:80
docker run --rm -it --network=host alpine ash -c "apk add socat && socat TCP-LISTEN:5000,reuseaddr,fork TCP:host.docker.internal:5000"


addon-operator module patches nginx
kubectl get crds -oname | xargs kubectl delete
```

### run

Build addon-operator image with custom scripts:

```
docker build -t "localhost:5000/addon-operator:poc1.1" .
docker push localhost:5000/addon-operator:poc1.1
```

Edit image in addon-operator-pod.yaml and apply manifests:

```
kubectl create ns example-module-sysctl-tuner
kubectl -n example-module-sysctl-tuner apply -f addon-operator-rbac.yaml
kubectl -n example-module-sysctl-tuner apply -f addon-operator-cm.yaml
kubectl -n example-module-sysctl-tuner apply -f addon-operator-pod.yaml
```

See in logs that helm release was successful and hook.sh was run as expected:

```
kubectl -n example-module-sysctl-tuner logs pod/addon-operator -f
...
INFO     : TASK_RUN ModuleRun sysctl-tuner
INFO     : Running module hook '001-sysctl-tuner/hooks/module-hooks.sh' binding 'BEFORE_HELM' ...
Run 'beforeHelm' hook for sysctl-tuner
INFO     : Running helm upgrade for release 'sysctl-tuner' with chart '/tmp/addon-operator/sysctl-tuner.chart' in namespace 'example-module-sysctl-tuner' ...
INFO     : Helm upgrade for release 'sysctl-tuner' with chart '/tmp/addon-operator/sysctl-tuner.chart' in namespace 'example-module-sysctl-tuner' successful:
Release "sysctl-tuner" has been upgraded. Happy Helming!
LAST DEPLOYED: Fri Apr 12 14:04:02 2019
NAMESPACE: example-module-sysctl-tuner
STATUS: DEPLOYED

RESOURCES:
==> v1beta1/DaemonSet
NAME          DESIRED  CURRENT  READY  UP-TO-DATE  AVAILABLE  NODE SELECTOR  AGE
sysctl-tuner  3        3        3      3           3          <none>         75s

==> v1/Pod(related)
NAME                READY  STATUS   RESTARTS  AGE
sysctl-tuner-6dh57  1/1    Running  0         75s
sysctl-tuner-9n69x  1/1    Running  0         75s
sysctl-tuner-p4q5p  1/1    Running  0         75s
INFO     : Running module hook '001-sysctl-tuner/hooks/module-hooks.sh' binding 'AFTER_HELM' ...
Run 'afterHelm' hook for sysctl-tuner
...
```

### enabling/disabling module

You can disable this module by editing cm/addon-operator:

```
kubectl -n example-module-sysctl-tuner edit cm/addon-operator

data:
  sysctlTunerEnabled: "false"
```

```
...
INFO     : TASK_RUN ModuleDelete sysctl-tuner
INFO     : Running module hook '001-sysctl-tuner/hooks/module-hooks.sh' binding 'AFTER_DELETE_HELM' ...
Run 'afterDeleteHelm' hook for sysctl-tuner
...
```

You can enable this module by editing cm/addon-operator:

```
kubectl -n example-module-sysctl-tuner edit cm/addon-operator

data:
  sysctlTunerEnabled: "true"
```


### cleanup

```
kubectl delete clusterrolebinding/addon-operator
kubectl delete clusterrole/addon-operator
kubectl delete ns/example-module-sysctl-tuner
docker rmi registry.mycompany.com/addon-operator:module-sysctl-tuner
```
