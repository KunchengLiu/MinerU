## **Mineru WebUI 启动脚本 (start\_webui.bat) 使用说明**

本脚本专用于启动 Mineru 的 WebUI（基于 Gradio）服务，它自动化了环境激活和变量设置的过程。

### **前提条件**

1. **已安装 Conda** (Anaconda 或 Miniconda)。  
2. **已完成 Mineru 的所有安装步骤**：包括创建名为 mineru 的环境，安装 PyTorch 和 Mineru 依赖。  
3. **Conda 初始化**：如果您是从 Windows 的**普通命令提示符 (CMD)** 启动此脚本，您需要确保已运行过一次 conda init 命令，以便系统识别 conda 命令。如果您从 **Anaconda Prompt** 启动则无需担心。

### **使用方法**

1. 将 start\_webui.bat 文件保存到您方便访问的目录。  
2. **双击运行** start\_webui.bat 文件。

### **脚本执行流程**

1. 脚本自动调用 conda activate mineru 激活 Mineru 虚拟环境。  
2. 脚本设置环境变量 MINERU\_MODEL\_SOURCE 为 modelscope。  
3. 脚本执行 mineru-gradio \--server-name 0.0.0.0 \--server-port 7860 启动 WebUI 服务。  
4. 服务启动后，您可以通过浏览器访问控制台显示的地址，默认为 http://127.0.0.1:7860。

### **提示**

* 服务启动后，命令行窗口会保持开启并显示运行日志。请不要关闭此窗口，否则服务将停止。  
* 如果您想修改环境名称或端口号，可以直接编辑 .bat 文件中的 set 变量。

# API 脚本使用指南 (call_mineru_api.py)

调用 Mineru API 服务。

如何使用此脚本

### 第一步：确保 API 正在运行

此脚本不会启动 Mineru 服务。您必须首先启动您的 API 服务，例如通过运行 start_mineru.bat 并选择 选项 1 (API 模式)。

确保该服务正在 http://127.0.0.1:8000 上运行。

### 第二步：安装 Python 依赖库

此脚本需要 requests 库，这是 Python 中用于发送 HTTP 请求的标准库。

在您的命令提示符 (CMD) 或终端中运行：

pip install requests


### 第三步：(最重要) 查找您的 API 文档

我提供的脚本使用了假设的端点 (/api/v1/process) 和假设的数据 ({"text_input": ...})。这些在您的 Mineru 服务上几乎肯定是不正确的。

您必须自己找到真实的 API 规格：

启动 Mineru API 服务 (mineru-api ...)。

在您的浏览器中打开 API 文档地址：http://127.0.0.1:8000/docs

这个页面（由 FastAPI 自动生成）会列出所有可用的 API 路径（例如 /api/v1/generate）、它们接受的方法（GET 或 POST）以及它们需要的确切 JSON 数据格式。

### 第四步：修改并运行脚本

编辑 call_mineru_api.py 脚本：

将 HYPOTHETICAL_ENDPOINT 变量（例如 /api/v1/process）更改为您在 /docs 页面上找到的真实路径。

修改 payload 字典，使其与 /docs 页面上要求的确切 JSON 结构相匹配。

运行脚本：

打开一个新的 CMD 或终端窗口（不要关闭正在运行 Mineru API 的窗口）。

运行脚本：python call_mineru_api.py

脚本将连接到正在运行的 API 服务，发送您指定的数据，并打印出服务返回的 JSON 结果。

