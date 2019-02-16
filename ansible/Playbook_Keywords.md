## Playbook Keywords

These are the keywords available on common playbook objects.

Please note:

* Aliases for the directives are not reflected here, nor are mutable one. For example, action in task can be substituted by the name of any Ansible module.

* The keywords do not have version_added information at this time

* Some keywords set defaults for the objects inside of them rather than for the objects themselves

### Play

* any_errors_fatal

Force any un-handled task errors on any host to propagate to all hosts and end the play.  强制任何主机上的任何未处理任务错误传播到所有主机并结束播放。

* become

Boolean that controls if privilege escalation is used or not on Task execution.  布尔值，用于控制是否在任务执行时使用权限升级。

* become_flags

A string of flag(s) to pass to the privilege escalation program when become is True.

* become_method

Which method of privilege escalation to use (such as sudo or su).

* become_user

User that you ‘become’ after using privilege escalation. The remote/login user must have permissions to become this user.  使用权限升级后您“成为”的用户。 远程/登录用户必须具有成为此用户的权限。

* check_mode

A boolean that controls if a task is executed in ‘check’ mode

See also Check Mode (“Dry Run”)

* connection

Allows you to change the connection plugin used for tasks to execute on the target.

See also Using Connection Plugins

* debugger

Enable debugging tasks based on state of the task result. See Playbook Debugger

* diff

Toggle to make tasks return ‘diff’ information or not.  切换以使任务返回'diff'信息与否。

* environment

A dictionary that gets converted into environment vars to be provided for the task upon execution.  转换为环境变量的字典，在执行时为任务提供。

* fact_path

Set the fact path option for the fact gathering plugin controlled by gather_facts.

* force_handlers

Will force notified handler execution for hosts even if they failed during the play. Will not trigger if the play itself fails.

* gather_facts

A boolean that controls if the play will automatically run the ‘setup’ task to gather facts for the hosts.

* gather_subset

Allows you to pass subset options to the fact gathering plugin controlled by gather_facts.

* gather_timeout

Allows you to set the timeout for the fact gathering plugin controlled by gather_facts.

* handlers

A section with tasks that are treated as handlers, these won’t get executed normally, only when notified after each section of tasks is complete.

* hosts

A list of groups, hosts or host pattern that translates into a list of hosts that are the play’s target.

* ignore_errors

Boolean that allows you to ignore task failures and continue with play. It does not affect connection errors.

* ignore_unreachable

Boolean that allows you to ignore unreachable hosts and continue with play. This does not affect other task errors (see ignore_errors) but is useful for groups of volatile/ephemeral hosts.

* max_fail_percentage

can be used to abort the run after a given percentage of hosts in the current batch has failed.  可以用于在当前批次中给定百分比的主机发生故障后中止运行。

* module_defaults

Specifies default parameter values for modules.

* name
Identifier. Can be used for documentation, in or tasks/handlers.

* no_log

Boolean that controls information disclosure.  控制信息泄露的布尔值。

* order

Controls the sorting of hosts as they are used for executing the play. Possible values are inventory (default), sorted, reverse_sorted, reverse_inventory and shuffle.

* port

Used to override the default port used in a connection.

* post_tasks

A list of tasks to execute after the tasks section.

* pre_tasks

A list of tasks to execute before roles.

* remote_user

User used to log into the target via the connection plugin.

* roles

List of roles to be imported into the play

* run_once

Boolean that will bypass the host loop, forcing the task to attempt to execute on the first host available and afterwards apply any results and facts to all active hosts in the same batch.  布尔值，它将绕过主机循环，强制任务尝试在第一个可用主机上执行，然后将任何结果和事实应用于同一批次中的所有活动主机。

* serial

Explicitly define how Ansible batches the execution of the current play on the play’s target.  明确定义

See also Rolling Update Batch Size

* strategy

Allows you to choose the connection plugin to use for the play.

* tags

Tags applied to the task or included tasks, this allows selecting subsets of tasks from the command line.

* tasks

Main list of tasks to execute in the play, they run after roles and before post_tasks.

* vars

Dictionary/map of variables

* vars_files

List of files that contain vars to include in the play.

* vars_prompt

list of variables to prompt for.

### Role

* any_errors_fatal

Force any un-handled task errors on any host to propagate to all hosts and end the play.

* become

Boolean that controls if privilege escalation is used or not on Task execution.

* become_flags

A string of flag(s) to pass to the privilege escalation program when become is True.

* become_method

Which method of privilege escalation to use (such as sudo or su).

* become_user

User that you ‘become’ after using privilege escalation. The remote/login user must have permissions to become this user.

* check_mode

A boolean that controls if a task is executed in ‘check’ mode

See also Check Mode (“Dry Run”)

* connection

Allows you to change the connection plugin used for tasks to execute on the target.

See also Using Connection Plugins

* debugger

Enable debugging tasks based on state of the task result. See Playbook Debugger

* delegate_facts

Boolean that allows you to apply facts to a delegated host instead of inventory_hostname.  布尔值，允许您将事实应用于委托主机而不是inventory_hostname。

* delegate_to

Host to execute task instead of the target (inventory_hostname). Connection vars from the delegated host will also be used for the task.

* diff

Toggle to make tasks return ‘diff’ information or not.

* environment

A dictionary that gets converted into environment vars to be provided for the task upon execution.

* ignore_errors

Boolean that allows you to ignore task failures and continue with play. It does not affect connection errors.

* ignore_unreachable

Boolean that allows you to ignore unreachable hosts and continue with play. This does not affect other task errors (see ignore_errors) but is useful for groups of volatile/ephemeral hosts.

* module_defaults

Specifies default parameter values for modules.

* name

Identifier. Can be used for documentation, in or tasks/handlers.

* no_log

Boolean that controls information disclosure.

* port

Used to override the default port used in a connection.

* remote_user

User used to log into the target via the connection plugin.

* run_once

Boolean that will bypass the host loop, forcing the task to attempt to execute on the first host available and afterwards apply any results and facts to all active hosts in the same batch.

* tags

Tags applied to the task or included tasks, this allows selecting subsets of tasks from the command line.

* vars

Dictionary/map of variables

* when

Conditional expression, determines if an iteration of a task is run or not.

### Block 

* always

List of tasks, in a block, that execute no matter if there is an error in the block or not.

* any_errors_fatal

Force any un-handled task errors on any host to propagate to all hosts and end the play.

* become

Boolean that controls if privilege escalation is used or not on Task execution.

* become_flags

A string of flag(s) to pass to the privilege escalation program when become is True.

* become_method

Which method of privilege escalation to use (such as sudo or su).

* become_user

User that you ‘become’ after using privilege escalation. The remote/login user must have permissions to become this user.

* block

List of tasks in a block.

* check_mode

A boolean that controls if a task is executed in ‘check’ mode

See also Check Mode (“Dry Run”)

* connection

Allows you to change the connection plugin used for tasks to execute on the target.

See also Using Connection Plugins

* debugger

Enable debugging tasks based on state of the task result. See Playbook Debugger

* delegate_facts

Boolean that allows you to apply facts to a delegated host instead of inventory_hostname.

* delegate_to

Host to execute task instead of the target (inventory_hostname). Connection vars from the delegated host will also be used for the task.

* diff

Toggle to make tasks return ‘diff’ information or not.

* environment

A dictionary that gets converted into environment vars to be provided for the task upon execution.

* ignore_errors

Boolean that allows you to ignore task failures and continue with play. It does not affect connection errors.

* ignore_unreachable

Boolean that allows you to ignore unreachable hosts and continue with play. This does not affect other task errors (see ignore_errors) but is useful for groups of volatile/ephemeral hosts.

* module_defaults

Specifies default parameter values for modules.

* name

Identifier. Can be used for documentation, in or tasks/handlers.

* no_log

Boolean that controls information disclosure.

* port

Used to override the default port used in a connection.

* remote_user

User used to log into the target via the connection plugin.

* rescue

List of tasks in a block that run if there is a task error in the main block list.

* run_once

Boolean that will bypass the host loop, forcing the task to attempt to execute on the first host available and afterwards apply any results and facts to all active hosts in the same batch.

* tags

Tags applied to the task or included tasks, this allows selecting subsets of tasks from the command line.

* vars

Dictionary/map of variables

* when

Conditional expression, determines if an iteration of a task is run or not.

### Task

* action

The ‘action’ to execute for a task, it normally translates into a C(module) or action plugin.

* any_errors_fatal

Force any un-handled task errors on any host to propagate to all hosts and end the play.

* args

DEPRECATED, A secondary way to add arguments into a task. Takes a dictionary in which keys map to options and values.

* async

Run a task asynchronously if the C(action) supports this; value is maximum runtime in seconds.  异步运行任务; value是以秒为单位的最大运行时间

* become

Boolean that controls if privilege escalation is used or not on Task execution.

* become_flags

A string of flag(s) to pass to the privilege escalation program when become is True.

* become_method

Which method of privilege escalation to use (such as sudo or su).

* become_user

User that you ‘become’ after using privilege escalation. The remote/login user must have permissions to become this user.

* changed_when

Conditional expression that overrides the task’s normal ‘changed’ status.

* check_mode

A boolean that controls if a task is executed in ‘check’ mode

See also Check Mode (“Dry Run”)

* connection

Allows you to change the connection plugin used for tasks to execute on the target.

See also Using Connection Plugins

* debugger

Enable debugging tasks based on state of the task result. See Playbook Debugger

* delay

Number of seconds to delay between retries. This setting is only used in combination with until.

* delegate_facts

Boolean that allows you to apply facts to a delegated host instead of inventory_hostname.

* delegate_to

Host to execute task instead of the target (inventory_hostname). Connection vars from the delegated host will also be used for the task.

* diff

Toggle to make tasks return ‘diff’ information or not.

* environment

A dictionary that gets converted into environment vars to be provided for the task upon execution.

* failed_when

Conditional expression that overrides the task’s normal ‘failed’ status.

* ignore_errors

Boolean that allows you to ignore task failures and continue with play. It does not affect connection errors.

* ignore_unreachable

Boolean that allows you to ignore unreachable hosts and continue with play. This does not affect other task errors (see ignore_errors) but is useful for groups of volatile/ephemeral hosts.

* local_action

Same as action but also implies delegate_to: localhost

* loop

Takes a list for the task to iterate over, saving each list element into the item variable (configurable via loop_control)

* loop_control

Several keys here allow you to modify/set loop behaviour in a task.

See also Loop Control

* module_defaults

Specifies default parameter values for modules.

* name

Identifier. Can be used for documentation, in or tasks/handlers.

* no_log

Boolean that controls information disclosure.

* notify

List of handlers to notify when the task returns a ‘changed=True’ status.

* poll

Sets the polling interval in seconds for async tasks (default 10s).

* port

Used to override the default port used in a connection.

* register

Name of variable that will contain task status and module return data.

* remote_user

User used to log into the target via the connection plugin.

* retries

Number of retries before giving up in a until loop. This setting is only used in combination with until.

* run_once

Boolean that will bypass the host loop, forcing the task to attempt to execute on the first host available and afterwards apply any results and facts to all active hosts in the same batch.

* tags

Tags applied to the task or included tasks, this allows selecting subsets of tasks from the command line.

* until

This keyword implies a ‘retries loop’ that will go on until the condition supplied here is met or we hit the retries limit.

* vars

Dictionary/map of variables

* when

Conditional expression, determines if an iteration of a task is run or not.

* with_<lookup_plugin>

The same as loop but magically adds the output of any lookup plugin to generate the item list.


1. volatile/ephemeral hosts.
2. delegate_facts
3. delegate_to
4. run_once
5. debugger
6. action
7. delay
8. local_action  本地操作功能
9. retries
10. until

[Ansible 性能优化、统计任务执行时间、SSH PIPElinING、Delegate_to( 任务委派功能 )、本地操作功能 --local_action](./Ansible_01.pdf)

[异步和轮询、Play执行时的并发限制、最大失败百分比、委托、委托者的facts、RUN ONCE](./Ansible_02.pdf)



