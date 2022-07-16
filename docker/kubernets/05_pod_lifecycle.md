# Pod Lifecycle

* https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/

This page describes the lifecycle of a Pod. Pods follow a defined lifecycle, starting in the `Pending`, moving through `Running` if at least one of its primary containers starts OK, and then through either the `Succeeded` or `Failed` phases depending on whether any container in the Pod terminated in failure.  本页描述了 Pod 的生命周期。 Pod 遵循定义的生命周期，从 Pending 阶段开始，如果至少一个主容器启动正常，则进入 Running，然后根据 Pod 中的任何容器是否因故障终止而进入 Succeeded 或 Failed 阶段。

Whilst a Pod is running, the kubelet is able to restart containers to handle some kind of faults. Within a Pod, Kubernetes tracks different container states and determines what action to take to make the Pod healthy again.  在 Pod 运行时，kubelet 能够重新启动容器以处理某种故障。 在 Pod 中，Kubernetes 会跟踪不同的容器状态，并确定采取什么行动来使 Pod 再次健康。

In the Kubernetes API, Pods have both a specification and an actual status. The status for a Pod object consists of a set of Pod conditions. You can also inject custom readiness information into the condition data for a Pod, if that is useful to your application.  在 Kubernetes API 中，Pod 既有规范又有实际状态。 Pod 对象的状态由一组 Pod 条件组成。 如果这对您的应用程序有用，您还可以将自定义就绪信息注入到 Pod 的条件数据中。

Pods are only [scheduled](https://kubernetes.io/docs/concepts/scheduling-eviction/) once in their lifetime. Once a Pod is scheduled (assigned) to a Node, the Pod runs on that Node until it stops or is terminated.  Pod 在其生命周期中只安排一次。 一旦 Pod 被调度（分配）给一个节点，该 Pod 就会在该节点上运行，直到它停止或终止。

## Pod lifetime

Like individual application containers, Pods are considered to be relatively ephemeral (rather than durable) entities. Pods are created, assigned a unique ID ([UID](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#uids)), and scheduled to nodes where they remain until termination (according to restart policy) or deletion. If a [Node](https://kubernetes.io/docs/concepts/architecture/nodes/) dies, the Pods scheduled to that node are scheduled for deletion after a timeout period.  与单个应用程序容器一样，Pod 被认为是相对短暂（而不是持久）的实体。 Pod 被创建，分配一个唯一的 ID (UID)，并被调度到节点上，直到终止（根据重启策略）或删除。如果一个 Node 死亡，调度到该节点的 Pod 会在超时后被调度删除。

Pods do not, by themselves, self-heal. If a Pod is scheduled to a [node](https://kubernetes.io/docs/concepts/architecture/nodes/) that then fails, the Pod is deleted; likewise, a Pod won't survive an eviction due to a lack of resources or Node maintenance. Kubernetes uses a higher-level abstraction, called a [controller](https://kubernetes.io/docs/concepts/architecture/controller/), that handles the work of managing the relatively disposable Pod instances.  Pod 本身不会自我修复。如果一个 Pod 被调度到一个失败的节点上，那么这个 Pod 就会被删除；同样，由于缺乏资源或节点维护，Pod 将无法生存。 Kubernetes 使用更高级别的抽象，称为控制器，它处理管理相对一次性的 Pod 实例的工作。

A given Pod (as defined by a UID) is never "rescheduled" to a different node; instead, that Pod can be replaced by a new, near-identical Pod, with even the same name if desired, but with a different UID.  给定的 Pod（由 UID 定义）永远不会“重新调度”到不同的节点；相反，该 Pod 可以替换为一个新的、几乎相同的 Pod，如果需要，甚至可以使用相同的名称，但具有不同的 UID。

When something is said to have the same lifetime as a Pod, such as a [volume](https://kubernetes.io/docs/concepts/storage/volumes/), that means that the thing exists as long as that specific Pod (with that exact UID) exists. If that Pod is deleted for any reason, and even if an identical replacement is created, the related thing (a volume, in this example) is also destroyed and created anew.  当说某物与 Pod 具有相同的生命周期时，例如卷，这意味着只要该特定 Pod（具有该确切 UID）存在，该物就存在。如果该 Pod 因任何原因被删除，即使创建了相同的替换，相关的事物（在此示例中为卷）也会被销毁并重新创建。

## Pod phase

A Pod's `status` field is a [PodStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podstatus-v1-core) object, which has a `phase` field.  Pod 的状态字段是一个 PodStatus 对象，它有一个阶段字段。

The phase of a Pod is a simple, high-level summary of where the Pod is in its lifecycle. The phase is not intended to be a comprehensive rollup of observations of container or Pod state, nor is it intended to be a comprehensive state machine.  Pod 的阶段是对 Pod 在其生命周期中所处位置的简单、高级摘要。 该阶段不是对容器或 Pod 状态观察的全面汇总，也不是一个全面的状态机。

The number and meanings of Pod phase values are tightly guarded. Other than what is documented here, nothing should be assumed about Pods that have a given `phase` value.  Pod 阶段值的数量和含义受到严格保护。 除了此处记录的内容外，不应假设 Pod 具有给定的相位值。

Here are the possible values for `phase`:  以下是相位的可能值：

| Value | Description |
| ----- | ----------- |
| `Pending` | The Pod has been accepted by the Kubernetes cluster, but one or more of the containers has not been set up and made ready to run. This includes time a Pod spends waiting to be scheduled as well as the time spent downloading container images over the network.   Pod 已被 Kubernetes 集群接受，但一个或多个容器尚未设置并准备好运行。 这包括 Pod 等待调度所花费的时间以及通过网络下载容器镜像所花费的时间。 |
| `Running` | The Pod has been bound to a node, and all of the containers have been created. At least one container is still running, or is in the process of starting or restarting.   Pod 已绑定到一个节点，并且所有容器都已创建。 至少有一个容器仍在运行，或者正在启动或重新启动过程中。 |
| `Succeeded` | All containers in the Pod have terminated in success, and will not be restarted.   Pod 中的所有容器都已成功终止，不会重新启动。 |
| `Failed` | All containers in the Pod have terminated, and at least one container has terminated in failure. That is, the container either exited with non-zero status or was terminated by the system.   Pod 中的所有容器都已终止，并且至少有一个容器因故障而终止。 也就是说，容器要么以非零状态退出，要么被系统终止。 |
| `Unknown` | For some reason the state of the Pod could not be obtained. This phase typically occurs due to an error in communicating with the node where the Pod should be running.   由于某种原因，无法获取 Pod 的状态。 此阶段通常是由于与应该运行 Pod 的节点通信时出错而发生的。|

> Note: When a Pod is being deleted, it is shown as `Terminating` by some kubectl commands. This `Terminating` status is not one of the Pod phases. A Pod is granted a term to terminate gracefully, which defaults to 30 seconds. You can use the flag `--force` to terminate a Pod by force.  当一个 Pod 被删除时，它被一些 kubectl 命令显示为 Terminating。 此终止状态不是 Pod 阶段之一。 Pod 被授予优雅终止的期限，默认为 30 秒。 您可以使用标志 --force 强制终止 Pod。

If a node dies or is disconnected from the rest of the cluster, Kubernetes applies a policy for setting the `phase` of all Pods on the lost node to Failed.  如果一个节点死亡或与集群的其余部分断开连接，Kubernetes 会应用策略将丢失节点上的所有 Pod 的阶段设置为 Failed。

## Container states

As well as the phase of the Pod overall, Kubernetes tracks the state of each container inside a Pod. You can use [container lifecycle hooks](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/) to trigger events to run at certain points in a container's lifecycle.  除了整个 Pod 的阶段，Kubernetes 还跟踪 Pod 内每个容器的状态。 您可以使用容器生命周期挂钩来触发事件以在容器生命周期的特定点运行。

Once the [scheduler](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/) assigns a Pod to a Node, the kubelet starts creating containers for that Pod using a [container runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes). There are three possible container states: `Waiting`, `Running`, and `Terminated`.  一旦调度程序将 Pod 分配给 Node，kubelet 就会开始使用容器运行时为该 Pod 创建容器。 存在三种可能的容器状态：Waiting、Running 和 Terminated。

To check the state of a Pod's containers, you can use `kubectl describe pod <name-of-pod>`. The output shows the state for each container within that Pod.  要检查 Pod 容器的状态，可以使用 kubectl describe pod <name-of-pod>。 输出显示该 Pod 中每个容器的状态。

Each state has a specific meaning:  每个状态都有特定的含义：

### `Waiting`

If a container is not in either the `Running` or `Terminated` state, it is `Waiting`. A container in the `Waiting` state is still running the operations it requires in order to complete start up: for example, pulling the container image from a container image registry, or applying [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) data. When you use `kubectl` to query a Pod with a container that is `Waiting`, you also see a Reason field to summarize why the container is in that state.  如果容器既不处于运行状态也不处于终止状态，则它处于等待状态。处于 Waiting 状态的容器仍在运行完成启动所需的操作：例如，从容器镜像注册表中拉取容器镜像，或应用 Secret 数据。当您使用 kubectl 查询具有正在等待的容器的 Pod 时，您还会看到一个原因字段来总结容器处于该状态的原因。

### `Running`

The `Running` status indicates that a container is executing without issues. If there was a `postStart` hook configured, it has already executed and finished. When you use `kubectl` to query a Pod with a container that is `Running`, you also see information about when the container entered the `Running` state.  Running 状态表示容器正在执行而没有问题。如果配置了 postStart 挂钩，则它已经执行并完成。当您使用 kubectl 查询具有正在运行的容器的 Pod 时，您还会看到有关容器何时进入运行状态的信息。

### `Terminated`

A container in the `Terminated` state began execution and then either ran to completion or failed for some reason. When you use `kubectl` to query a Pod with a container that is `Terminated`, you see a reason, an exit code, and the start and finish time for that container's period of execution.  处于 Terminated 状态的容器开始执行，然后运行完成或由于某种原因失败。当您使用 kubectl 查询具有已终止容器的 Pod 时，您会看到原因、退出代码以及该容器执行期间的开始和结束时间。

If a container has a `preStop` hook configured, this hook runs before the container enters the `Terminated` state.  如果容器配置了 preStop 钩子，则该钩子在容器进入 Terminated 状态之前运行。

## Container restart policy

The `spec` of a Pod has a `restartPolicy` field with possible values Always, OnFailure, and Never. The default value is Always.

The `restartPolicy` applies to all containers in the Pod. `restartPolicy` only refers to restarts of the containers by the kubelet on the same node. After containers in a Pod exit, the kubelet restarts them with an exponential back-off delay (10s, 20s, 40s, …), that is capped at five minutes. Once a container has executed for 10 minutes without any problems, the kubelet resets the restart backoff timer for that container.

## Pod conditions

A Pod has a PodStatus, which has an array of [PodConditions](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#podcondition-v1-core) through which the Pod has or has not passed:

- `PodScheduled`: the Pod has been scheduled to a node.  Pod 已被调度到某个节点。

- `ContainersReady`: all containers in the Pod are ready.  Pod 中的所有容器都准备好了。

- `Initialized`: all [init containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) have completed successfully.  所有初始化容器均已成功完成。

- `Ready`: the Pod is able to serve requests and should be added to the load balancing pools of all matching Services.  Pod 能够服务请求，应该添加到所有匹配服务的负载均衡池中。

| Field name | Description |
| ---------- | ----------- |
| `type` | Name of this Pod condition. |
| `status` | Indicates whether that condition is applicable, with possible values "`True`", "`False`", or "`Unknown`". |
| `lastProbeTime` | Timestamp of when the Pod condition was last probed. |
| `lastTransitionTime` | Timestamp for when the Pod last transitioned from one status to another. |
| `reason` | Machine-readable, UpperCamelCase text indicating the reason for the condition's last transition. |
| `message` | Human-readable message indicating details about the last status transition. |

### Pod readiness

**FEATURE STATE:** `Kubernetes v1.14 [stable]`

Your application can inject extra feedback or signals into PodStatus: *Pod readiness*. To use this, set `readinessGates` in the Pod's `spec` to specify a list of additional conditions that the kubelet evaluates for Pod readiness.

Readiness gates are determined by the current state of `status.condition` fields for the Pod. If Kubernetes cannot find such a condition in the `status.conditions` field of a Pod, the status of the condition is defaulted to "`False`".

Here is an example:

```yaml
kind: Pod
...
spec:
  readinessGates:
    - conditionType: "www.example.com/feature-1"
status:
  conditions:
    - type: Ready # a built in PodCondition
      status: "False"
      lastProbeTime: null
      lastTransitionTime: 2018-01-01T00:00:00Z
    - type: "www.example.com/feature-1" # an extra PodCondition
      status: "False"
      lastProbeTime: null
      lastTransitionTime: 2018-01-01T00:00:00Z
  containerStatuses:
    - containerID: docker://abcd...
      ready: true
...
```

The Pod conditions you add must have names that meet the Kubernetes [label key format](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#syntax-and-character-set).

### Status for Pod readiness

The `kubectl patch` command does not support patching object status. To set these `status.conditions` for the pod, applications and [operators](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) should use the `PATCH` action. You can use a [Kubernetes client library](https://kubernetes.io/docs/reference/using-api/client-libraries/) to write code that sets custom Pod conditions for Pod readiness.

For a Pod that uses custom conditions, that Pod is evaluated to be ready **only** when both the following statements apply:

- All containers in the Pod are ready.
- All conditions specified in `readinessGates` are `True`.

When a Pod's containers are Ready but at least one custom condition is missing or `False`, the kubelet sets the Pod's condition to `ContainersReady`.

## Container probes

A *probe* is a diagnostic performed periodically by the [kubelet](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/) on a container. To perform a diagnostic, the kubelet either executes code within the container, or makes a network request.

### Check mechanisms

There are four different ways to check a container using a probe. Each probe must define exactly one of these four mechanisms:

`exec`

Executes a specified command inside the container. The diagnostic is considered successful if the command exits with a status code of 0.

`grpc`

Performs a remote procedure call using [gRPC](https://grpc.io/). The target should implement [gRPC health checks](https://grpc.io/grpc/core/md_doc_health-checking.html). The diagnostic is considered successful if the `status` of the response is `SERVING`.

gRPC probes are an alpha feature and are only available if you enable the `GRPCContainerProbe` [feature gate](https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/).

`httpGet`

Performs an HTTP `GET` request against the Pod's IP address on a specified port and path. The diagnostic is considered successful if the response has a status code greater than or equal to 200 and less than 400.

`tcpSocket`

Performs a TCP check against the Pod's IP address on a specified port. The diagnostic is considered successful if the port is open. If the remote system (the container) closes the connection immediately after it opens, this counts as healthy.

### Probe outcome

Each probe has one of three results:

`Success`

The container passed the diagnostic.

`Failure`

The container failed the diagnostic.

`Unknown`

The diagnostic failed (no action should be taken, and the kubelet will make further checks).

### Types of probe

The kubelet can optionally perform and react to three kinds of probes on running containers:

`livenessProbe`

Indicates whether the container is running. If the liveness probe fails, the kubelet kills the container, and the container is subjected to its restart policy. If a container does not provide a liveness probe, the default state is `Success`.

`readinessProbe`

Indicates whether the container is ready to respond to requests. If the readiness probe fails, the endpoints controller removes the Pod's IP address from the endpoints of all Services that match the Pod. The default state of readiness before the initial delay is `Failure`. If a container does not provide a readiness probe, the default state is `Success`.

`startupProbe`

Indicates whether the application within the container is started. All other probes are disabled if a startup probe is provided, until it succeeds. If the startup probe fails, the kubelet kills the container, and the container is subjected to its restart policy. If a container does not provide a startup probe, the default state is `Success`.

For more information about how to set up a liveness, readiness, or startup probe, see [Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).

#### When should you use a liveness probe?

**FEATURE STATE:** `Kubernetes v1.0 [stable]`

If the process in your container is able to crash on its own whenever it encounters an issue or becomes unhealthy, you do not necessarily need a liveness probe; the kubelet will automatically perform the correct action in accordance with the Pod's `restartPolicy`.

If you'd like your container to be killed and restarted if a probe fails, then specify a liveness probe, and specify a `restartPolicy` of Always or OnFailure.

#### When should you use a readiness probe?

**FEATURE STATE:** `Kubernetes v1.0 [stable]`

If you'd like to start sending traffic to a Pod only when a probe succeeds, specify a readiness probe. In this case, the readiness probe might be the same as the liveness probe, but the existence of the readiness probe in the spec means that the Pod will start without receiving any traffic and only start receiving traffic after the probe starts succeeding.

If you want your container to be able to take itself down for maintenance, you can specify a readiness probe that checks an endpoint specific to readiness that is different from the liveness probe.

If your app has a strict dependency on back-end services, you can implement both a liveness and a readiness probe. The liveness probe passes when the app itself is healthy, but the readiness probe additionally checks that each required back-end service is available. This helps you avoid directing traffic to Pods that can only respond with error messages.

If your container needs to work on loading large data, configuration files, or migrations during startup, you can use a startup probe. However, if you want to detect the difference between an app that has failed and an app that is still processing its startup data, you might prefer a readiness probe.

> Note: If you want to be able to drain requests when the Pod is deleted, you do not necessarily need a readiness probe; on deletion, the Pod automatically puts itself into an unready state regardless of whether the readiness probe exists. The Pod remains in the unready state while it waits for the containers in the Pod to stop.

#### When should you use a startup probe?

**FEATURE STATE:** `Kubernetes v1.20 [stable]`

Startup probes are useful for Pods that have containers that take a long time to come into service. Rather than set a long liveness interval, you can configure a separate configuration for probing the container as it starts up, allowing a time longer than the liveness interval would allow.

If your container usually starts in more than `initialDelaySeconds + failureThreshold × periodSeconds`, you should specify a startup probe that checks the same endpoint as the liveness probe. The default for `periodSeconds` is 10s. You should then set its `failureThreshold` high enough to allow the container to start, without changing the default values of the liveness probe. This helps to protect against deadlocks.

## Termination of Pods

Because Pods represent processes running on nodes in the cluster, it is important to allow those processes to gracefully terminate when they are no longer needed (rather than being abruptly stopped with a `KILL` signal and having no chance to clean up).  因为 Pod 代表在集群中的节点上运行的进程，所以允许这些进程在不再需要它们时优雅地终止（而不是通过 KILL 信号突然停止并且没有机会清理）是很重要的。

The design aim is for you to be able to request deletion and know when processes terminate, but also be able to ensure that deletes eventually complete. When you request deletion of a Pod, the cluster records and tracks the intended grace period before the Pod is allowed to be forcefully killed. With that forceful shutdown tracking in place, the [kubelet](https://kubernetes.io/docs/reference/generated/kubelet) attempts graceful shutdown.  设计目标是让您能够请求删除并知道进程何时终止，而且还能够确保删除最终完成。当您请求删除 Pod 时，集群会记录并跟踪允许强制杀死 Pod 之前的预期宽限期。随着强制关闭跟踪到位，kubelet 尝试正常关闭。

Typically, the container runtime sends a TERM signal to the main process in each container. Many container runtimes respect the `STOPSIGNAL` value defined in the container image and send this instead of TERM. Once the grace period has expired, the KILL signal is sent to any remaining processes, and the Pod is then deleted from the [API Server](https://kubernetes.io/docs/concepts/overview/components/#kube-apiserver). If the kubelet or the container runtime's management service is restarted while waiting for processes to terminate, the cluster retries from the start including the full original grace period.  通常，容器运行时向每个容器中的主进程发送一个 TERM 信号。许多容器运行时尊重容器映像中定义的 STOPSIGNAL 值，并发送此值而不是 TERM。一旦宽限期到期，KILL 信号就会发送到任何剩余的进程，然后 Pod 会从 API Server 中删除。如果 kubelet 或容器运行时的管理服务在等待进程终止时重新启动，则集群会从头开始重试，包括完整的原始宽限期。

An example flow:

1. You use the `kubectl` tool to manually delete a specific Pod, with the default grace period (30 seconds).

2. The Pod in the API server is updated with the time beyond which the Pod is considered "dead" along with the grace period. If you use `kubectl describe` to check on the Pod you're deleting, that Pod shows up as "Terminating". On the node where the Pod is running: as soon as the kubelet sees that a Pod has been marked as terminating (a graceful shutdown duration has been set), the kubelet begins the local Pod shutdown process.

If one of the Pod's containers has defined a `preStop` [hook](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks), the kubelet runs that hook inside of the container. If the `preStop` hook is still running after the grace period expires, the kubelet requests a small, one-off grace period extension of 2 seconds.

> Note: If the `preStop` hook needs longer to complete than the default grace period allows, you must modify `terminationGracePeriodSeconds` to suit this.

The kubelet triggers the container runtime to send a TERM signal to process 1 inside each container.

> Note: The containers in the Pod receive the TERM signal at different times and in an arbitrary order. If the order of shutdowns matters, consider using a `preStop` hook to synchronize.

3. At the same time as the kubelet is starting graceful shutdown, the control plane removes that shutting-down Pod from Endpoints (and, if enabled, EndpointSlice) objects where these represent a [Service](https://kubernetes.io/docs/concepts/services-networking/service/) with a configured [selector](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/). [ReplicaSets](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/) and other workload resources no longer treat the shutting-down Pod as a valid, in-service replica. Pods that shut down slowly cannot continue to serve traffic as load balancers (like the service proxy) remove the Pod from the list of endpoints as soon as the termination grace period *begins*.

4. When the grace period expires, the kubelet triggers forcible shutdown. The container runtime sends `SIGKILL` to any processes still running in any container in the Pod. The kubelet also cleans up a hidden `pause` container if that container runtime uses one.

5. The kubelet triggers forcible removal of Pod object from the API server, by setting grace period to 0 (immediate deletion).

6. The API server deletes the Pod's API object, which is then no longer visible from any client.

### Forced Pod termination

**Caution:** Forced deletions can be potentially disruptive for some workloads and their Pods.

By default, all deletes are graceful within 30 seconds. The `kubectl delete` command supports the `--grace-period=<seconds>` option which allows you to override the default and specify your own value.

Setting the grace period to `0` forcibly and immediately deletes the Pod from the API server. If the pod was still running on a node, that forcible deletion triggers the kubelet to begin immediate cleanup.

**Note:** You must specify an additional flag `--force` along with `--grace-period=0` in order to perform force deletions.

When a force deletion is performed, the API server does not wait for confirmation from the kubelet that the Pod has been terminated on the node it was running on. It removes the Pod in the API immediately so a new Pod can be created with the same name. On the node, Pods that are set to terminate immediately will still be given a small grace period before being force killed.

If you need to force-delete Pods that are part of a StatefulSet, refer to the task documentation for [deleting Pods from a StatefulSet](https://kubernetes.io/docs/tasks/run-application/force-delete-stateful-set-pod/).

### Garbage collection of failed Pods

For failed Pods, the API objects remain in the cluster's API until a human or [controller](https://kubernetes.io/docs/concepts/architecture/controller/) process explicitly removes them.

The control plane cleans up terminated Pods (with a phase of `Succeeded` or `Failed`), when the number of Pods exceeds the configured threshold (determined by `terminated-pod-gc-threshold` in the kube-controller-manager). This avoids a resource leak as Pods are created and terminated over time.

## What's next

- Get hands-on experience [attaching handlers to container lifecycle events](https://kubernetes.io/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/).

- Get hands-on experience [configuring Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).

- Learn more about [container lifecycle hooks](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/).

- For detailed information about Pod and container status in the API, see the API reference documentation covering [`.status`](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#PodStatus) for Pod.


