# AutoGan

## 介绍

AutoGan 是一个 agent frame，它为大规模 agent 群组和超长工作流而设计。
通过 AutoGan 可以将 agent 和真人员工结合，形成一系列独立的数字部门。
这些部门可以独立运作，同时又能在需要的时候，让 agent、真人员工、数字部门之间互相协作，以完成各种任务。
我们的目标是创造一个环境，能够充分发掘和利用 LLM 的最大潜力。
随着 LLM 的不断发展和进步，相信越来越多的人工任务将被接替。

* 每个 agent 可以自主选择需要交流的对象。
* 除了依赖于 LLM 本身的能力，agent 还可以借助工具函数实现更多功能，例如：代码执行、数据查询、文件读取、邮件发送等。
* 通过构建组织架构，可以将 agent 和真人员工组成数字部门，并定义各数字部门的上下级关系。
* 在默认情况下，agent 的协作对象只限于当前部门的其他 agent 或真人员工，以及子数字部门的 leader。
* agent 在执行任务时，可根据需要向其他 agent、真人员工或数字部门的 leader 发布子任务。
* agent 的对话域仅聚焦于当前任务，不会受到其他任务对话内容的影响。
* 如果一个任务的执行过程较长，那么远期的会话记录将被压缩，但任务的原始内容将始终保持不变。

## Quickstart

### install
AutoGan requires Python version >= 3.8. It can be installed from pip:

```shell
pip install pyautogan
```

### notebook
在 jupyter 中运行已创建的示例

1. 下载本仓库
    ```shell
    git clone 
    cd autogan/notebook
    ```
2. 打开 ./notebook 中的 LLM_CONFIG 文件，然后设置正确的配置
3. 开始运行 notebook

如需要 agent 执行代码，请使用 docker 环境

## 特性

### Agent
在本框架中，agent 可以是以 LLM 为核心的智能体，也可以是仅使用工具函数的自动化程序，或者是真人员工的数字化身。

所有 agent 都是在 UniversalAgent 基类之上构建的，其主要属性如下：

* **name:** 该属性相当于 agent 的地址，用于 agent 之间的相互识别与沟通，因此该属性的值应当是全局唯一的。
* **duty:** 用于向其他 agent 介绍自身职责及能力。
* **work_flow:** 用于定义 agent 自身的工作流程。
* **use_tool** 用于定义 agent 使用工具函数的方式。

框架本身已构建了一些基础的 agent，实现了网络查询、编程、邮件发送等功能，以便于用户可以快速上手。

关于 agent 的详细介绍和创建方法，可参考 notebook

### 工具使用
如想要为 agent 添加定制化功能，可以通过重写 UniversalAgent 类的 tool_function 方法来实现。

* agent 的 use_tool 属性，与 tool_function 方法的调用关系：

   | use_tool   | tool_function         |
   |:-----------|-----------------------|
   | None       | 不调用工具函数               |
   | only       | 不使用 LLM，仅调用工具函数生成结果。  |
   | join       | LLM 生成的内容将作为工具函数的输入参数 |

关于 agent 工具使用的详细介绍，可参考 notebook

### 组织架构
考虑到并非所有 agent 之间都需要建立协作关系，且过多无用的协作关系会影响到 agent 决策的准确性。
因此本框架引入了组织架构的概念，让需要相互协作的 agent 组成独立的数字部门，以更加专注于解决特定领域的问题。

创建组织架构的方式非常简单，只需要定义一个存储 agent 对象的多维列表，例如：
```python
org_structure = [customer, customer_manager, 
                    [project_manager, product_manager
                        [coder, code_execution_agent]
                     ]
                ]
```
数字部门支持上下级关系，各部门的第一个 agent 为部门的 leader，其负责与上级部门的 agent 进行沟通。
因此 leader 的 duty 属性应当概述整个部门的职测与能力。

### 会话域
agent 之间的协作，是以任务为基础的，一个任务通常会被 agent 查分成多个子任务后，再分派给其他 agent。
每轮对话中 agent 仅会专注于当前任务内，有其参与的会话内容。
任何 agent 不会受到上级任务或子任务执行过程的影响。

### Switch
所有 agent 的回复消息，都会先被推送到 Switch，Switch 本身不会决定消息的接收方，
而是通过消息内的 @ 符号来判断将消息转发给谁。

除此之外，Switch 还负责任务的创建和任务间所属关系的维护。
