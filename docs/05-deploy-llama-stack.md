# 🤖 Deploy LLaMA Stack with MCP Integration

This section covers integrating everything together using the LLaMA Stack Operator to deploy and manage LLMs.

## Overview

Learn how to deploy the LLaMA Stack on OpenShift and integrate it with your MCP server, Gradio interface, and Milvus vector database to create a complete AI-powered Kubernetes management solution.

## Prerequisites

- Complete MCP server deployment on OpenShift
- Gradio interface deployed and accessible
- Milvus vector database running
- [OpenShift CLI (oc)](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)
- [Helm](https://helm.sh/docs/intro/install/) for package management

## What is LLaMA Stack?

The LLaMA Stack is a comprehensive solution for deploying and managing Large Language Models in Kubernetes environments. It provides:
- Model serving capabilities
- Inference optimization
- Model management and versioning
- Integration with vector databases
- RESTful API endpoints

## Deployment Steps


### 1. Install LLaMA Stack Operator

You can either deploy it manually into your cluster or install Red Hat OpenShift AI and enable the llama-stack operator.

### 2. Create a LlamaStackDistribution instance.

```bash
helm template llama-stack-chart \
  --set type=mcp \
  --set inference.model="$OLS_PROVIDER_MODEL_NAME" \
  --set inference.vllm.url="$OLS_PROVIDER_API_URL" \
  --set inference.vllm.tlsVerify="true" \
  --set inference.vllm.apiToken="$OLS_PROVIDER_API_TOKEN" \
  | oc apply -f -

```

Now, you can port forward the service to your local machine to test it.

```bash
oc port-forward service/llama-stack-service 8321:8321
```


### 3. Check the MCP server Swagger UI


>[!NOTE]
> Now that you are port forwarding the service, you can access the Llama Stack Swagger UI at [http://localhost:8321/docs](http://localhost:8321/docs).


### 4. Use the CLI to test your Llama Stack

First, you need to install the llama-stack-client:

```bash
source ~/venv/bin/activate
pip install llama-stack-client
```

Then, you can use it to test your Llama Stack:

```bash
# Get the version
llama-stack-client --version
> llama-stack-client, version 0.2.18

# Get the model list
llama-stack-client models list

# Get the toolgroups list
llama-stack-client toolgroups list

# Get the toolgroup details
llama-stack-client toolgroups get mcp::openshift

# Get the model details
llama-stack-client models get llama-3-2-3b 
> INFO:httpx:HTTP Request: GET http://localhost:8321/v1/models/llama-3-2-3b "HTTP/1.1 200 OK"
```

Finally, you can use the inference chat-completion to test your Llama Stack:

```bash
llama-stack-client inference chat-completion --message "Can you list me the pods of the cluster?"
```
This will return the response from the Llama Stack.

```bash
INFO:httpx:HTTP Request: GET http://localhost:8321/v1/models "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST http://localhost:8321/v1/openai/v1/chat/completions "HTTP/1.1 200 OK"
OpenAIChatCompletion(
    id='chatcmpl-4ba1af1e7e004130a966147465050035',
    choices=[
        OpenAIChatCompletionChoice(
            finish_reason='stop',
            index=0,
            message=OpenAIChatCompletionChoiceMessageOpenAIAssistantMessageParam(
                role='assistant',
                content="I'm sorry for the inconvenience, but as an AI, I don't have real-time access to your local or remote clusters, including Kubernetes or any other container orchestration platforms. To 
list the pods in your cluster, you would typically use a command-line interface like `kubectl` in a terminal, directing it to your Kubernetes cluster. Here's the basic command:\n\n`kubectl get pods`\n\nPlease 
ensure you have the Kubernetes command-line tool `kubectl` installed and configured to interact with your cluster before running this command. If you're using a managed Kubernetes service provided by a cloud 
provider like AWS (EKS), Google Cloud (GKE), or Azure (AKS), you might need to authenticate your `kubectl` with their CLI tools first.\n\nEvery cluster and its resource listings are unique to the specific setup 
and configurations, so the output could vary based on what pods are currently running or have been created in your cluster.\n\nIf you have access rights and are working within a command-line environment where 
`kubectl` is properly set up, running the above command should yield the list of pods. Any errors or issues obtaining this information would likely stem from misconfiguration, wrong context, or lack of 
permissions, not from the AI assistance I provide here.",
                name=None,
                tool_calls=None,
                refusal=None,
                annotations=None,
                audio=None,
                function_call=None,
                reasoning_content=None
            ),
            logprobs=None,
            stop_reason=None
        )
    ],
    created=1756076910,
    model='llama-3-2-3b',
    object='chat.completion',
    service_tier=None,
    system_fingerprint=None,
    usage={'completion_tokens': 264, 'prompt_tokens': 69, 'total_tokens': 333, 'completion_tokens_details': None, 'prompt_tokens_details': None},
    prompt_logprobs=None,
    kv_transfer_params=None
)
```


> [!IMPORTANT]  
> It's nice and simple, right? But as you can see, the tool directly calls the vllm server to get the response, so it's not a good idea to use when you want to vitamin the answer with some other tools, such as the MCP server. Let's see how to do that in the next section.


### 5. Use the Python SDK to test your Llama Stack fully

There are several blogs you should read before you start:

* [Exploring Llama Stack with Python: Tool calling and agents](https://developers.redhat.com/articles/2025/07/15/exploring-llama-stack-python-tool-calling-and-agents)
* [Level 5: Agents & MCP Tools](https://github.com/opendatahub-io/llama-stack-demos/blob/main/demos/rag_agentic/notebooks-output/Level5_agents_and_mcp.ipynb)
* [How to auth with Llama Stack MCP](https://medium.com/@gallettilance/how-to-auth-w-llama-stack-mcp-4a8631398555)
* [GitHub: Python AI Experimentation](https://github.com/mhdawson/python-ai-experimentation/tree/main)



```python
# WIP: Esto es un carajal
```



## Next Steps

Congratulations! You've completed the MCP Playground setup. Consider exploring:
- Advanced MCP server configurations
- Custom model fine-tuning
- Integration with additional data sources
- Performance optimization techniques

## 🎉 You've Completed the MCP Playground!

You now have a fully functional AI-powered Kubernetes management system running on OpenShift! 🚀
