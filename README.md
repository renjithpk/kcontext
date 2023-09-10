# kcontext - Kubernetes Context Selector

**kcontext** is a versatile tool designed to simplify the process of selecting Kubernetes contexts, allowing you to effortlessly switch between different clusters and namespaces. It enhances context selection by utilizing tags based on context names, making it quick and intuitive to identify and choose the context you need.

## Features

- **Tag-Based Context Selection**: kcontext introduces a novel way to select contexts by associating tags with context names. When you list your contexts, you will see tags displayed before each context name, making it easier to identify their purpose.

- **Color-Coded Tags**: To enhance visibility and distinction, kcontext color-codes the tags. Tags are displayed in the order they are defined, providing a clear visual hierarchy for your contexts.

- **Customizable Tagging**: You have the flexibility to customize the tagging to suit your preferences. By setting the `K_CONTEXT_TAGS_JSON` environment variable with your preferred key-value pairs in JSON format, you can tailor the tagging system to your specific needs.

    Example:
    ```bash
    export K_CONTEXT_TAGS_JSON='{
        "production": "[prod]",
        "development": "[dev]",
        "west": "[west]",
        "central": "[cent]"
    }'
    ```

    If you don't set the `K_CONTEXT_TAGS_JSON` environment variable, kcontext will use a default tag map that includes common tags like `[prod]` for production, `[dev]` for development, and others to represent different context types.

## Usage

1. **Installation**: To start using kcontext, you need to install it on your system. You can do this by following the installation instructions in the [installation guide](INSTALL.md).

2. **Configuration**: Customize your context tagging by setting the `K_CONTEXT_TAGS_JSON` environment variable as shown in the example above.

3. **Select Context**: Once installed and configured, simply run `kcontext` to see your list of Kubernetes contexts with tags. Use the displayed tags to quickly identify and choose the context you want.

## Contributions

We welcome contributions to kcontext. If you have ideas for improvements or encounter issues, please feel free to open an issue or submit a pull request on our [GitHub repository](https://github.com/your-repo-link).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

