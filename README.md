# Kraken

<h1 align="center">
  <br>
  <img src="https://raw.githubusercontent.com/kraken-ng/Kraken/main/static/kraken-logo-background.jpg" alt="Kraken">
</h1>

<h4 align="center">Kraken, a modular multi-language webshell coded by @secu_x11.</h4>

<p align="center">
  <a href="https://github.com/kraken-ng/Kraken/wiki/Getting-Started#requirements">Requirements</a> •
  <a href="https://github.com/kraken-ng/Kraken/wiki/Support">Support</a> •
  <a href="https://github.com/kraken-ng/Kraken/wiki/Getting-Started#installation">Install</a> •
  <a href="https://github.com/kraken-ng/Kraken/wiki/Getting-Started#usage">Usage</a> •
  <a href="https://github.com/kraken-ng/Kraken/wiki/Getting-Started#advanced-usage">Advanced Usage</a> •
  <a href="https://github.com/kraken-ng/Kraken/wiki/Contribute">Contributing</a> •
  <a href="https://github.com/kraken-ng/Kraken/wiki/FAQ-&-Troubleshooting">FAQ</a> •
  <a href="https://github.com/kraken-ng/Kraken/wiki/Acknowledgments-&-References">Acknowledgments</a>
</p>

---

Kraken is a modular multi-language webshell focused on web post-exploitation and defense evasion. It supports three technologies (**PHP, JSP and ASPX**) and is core is developed in Python.

Kraken follows the principle of <b><ins>"avoiding command execution"</ins></b> by re-implementing it through the functionalities of the programming language in use. Kraken seeks to provide usability, scalability and improve the OPSEC of ongoing operations.

Although its main use is focused on offensive purposes (e.g. red teams, internal pentest), it is possible to use it by blue teams to evaluate existing defensive tools and configurations.

## Version

1.0.0 - [Version CHANGELOG](CHANGELOG.md)

## Wiki

All the information about the functionality of the modules, the structure and the creation is explained in the [Github's Wiki]:

- **[I. Home]**
- **[II. Support]**
  - [Agents supported]
  - [Modules supported]
    - [Support on Linux]
    - [Support on Windows]
  - [Version testing]
- **[III. Getting Started]**
  - [Requirements]
  - [Installation]
    - [Installation on Linux]
    - [Installation on Windows]
    - [Installation on MacOS]
  - [Usage]
    - [Choosing the web technology]
    - [Choosing the environment]
    - [Deploying the environment]
    - [Modifying agent]
    - [Selecting a connection profile]
    - [Connection from client]
  - [Advanced Usage]
    - [Standard Mode]
      - [Using Java Agent]
      - [Using NET Agent]
    - [Command and control Mode]
- **[IV. Contribute]**
  - [Module contributions]
    - [Introduction]
    - [PHP Module Creation]
      - [PHP Template Structure]
      - [PHP Module Development]
      - [PHP Module Versioning]
      - [PHP Module Registration]
    - [Java Module Creation]
      - [Java Template Structure]
      - [Java Module Development]
      - [Java Module Versioning]
      - [Java Module Registration]
    - [NET Module Creation]
      - [NET Template Structure]
      - [NET Module Development]
      - [NET Module Versioning]
      - [NET Module Registration]
  - [Dispatcher contributions]
  - [Formater contributions]
  - [Environment contributions]
  - [Util contributions]
- **[V. Internals]**
- **[VI. FAQ & Troubleshooting]**
  - [Known bugs]
- **[VII. Acknowledgments & References]**
  - [Acknowledgments]
  - [References]




[Github's Wiki]: https://github.com/kraken-ng/Kraken/wiki
[I. Home]: https://github.com/kraken-ng/Kraken/wiki
[II. Support]: https://github.com/kraken-ng/Kraken/wiki/Support
[Agents supported]: https://github.com/kraken-ng/Kraken/wiki/Support#agents
[Modules supported]: https://github.com/kraken-ng/Kraken/wiki/Support#modules
[Support on Linux]: https://github.com/kraken-ng/Kraken/wiki/Support#support-on-linux
[Support on Windows]: https://github.com/kraken-ng/Kraken/wiki/Support#support-on-windows
[Version testing]: https://github.com/kraken-ng/Kraken/wiki/Support#version-testing
[III. Getting Started]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started
[Requirements]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#requirements
[Installation]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#installation
[Installation on Linux]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#installation-on-linux
[Installation on Windows]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#installation-on-windows
[Installation on MacOS]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#installation-on-macos
[Usage]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#usage
[Choosing the web technology]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#choosing-the-web-technology
[Choosing the environment]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#choosing-the-environment
[Deploying the environment]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#deploying-the-environment
[Modifying agent]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#modifying-agent
[Selecting a connection profile]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#selecting-a-connection-profile
[Connection from client]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#connection-from-client
[Advanced Usage]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#advanced-usage
[Standard Mode]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#standard-mode
[Using Java Agent]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#using-java-agent
[Using NET Agent]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#using-net-agent
[Command and control Mode]: https://github.com/kraken-ng/Kraken/wiki/Getting-Started#command-and-control-mode
[IV. Contribute]: https://github.com/kraken-ng/Kraken/wiki/Contribute
[Module contributions]: https://github.com/kraken-ng/Kraken/wiki/Contribute#modules
[Introduction]: https://github.com/kraken-ng/Kraken/wiki/Contribute#introduction
[PHP Module Creation]: https://github.com/kraken-ng/Kraken/wiki/Contribute#php-module-creation
[PHP Template Structure]: https://github.com/kraken-ng/Kraken/wiki/Contribute#php-template-structure
[PHP Module Development]: https://github.com/kraken-ng/Kraken/wiki/Contribute#php-module-development
[PHP Module Versioning]: https://github.com/kraken-ng/Kraken/wiki/Contribute#php-module-versioning
[PHP Module Registration]: https://github.com/kraken-ng/Kraken/wiki/Contribute#php-module-registration
[Java Module Creation]: https://github.com/kraken-ng/Kraken/wiki/Contribute#java-module-creation
[Java Template Structure]: https://github.com/kraken-ng/Kraken/wiki/Contribute#java-template-structure
[Java Module Development]: https://github.com/kraken-ng/Kraken/wiki/Contribute#java-module-development
[Java Module Versioning]: https://github.com/kraken-ng/Kraken/wiki/Contribute#java-module-versioning
[Java Module Registration]: https://github.com/kraken-ng/Kraken/wiki/Contribute#java-module-registration
[NET Module Creation]: https://github.com/kraken-ng/Kraken/wiki/Contribute#net-module-creation
[NET Template Structure]: https://github.com/kraken-ng/Kraken/wiki/Contribute#net-template-structure
[NET Module Development]: https://github.com/kraken-ng/Kraken/wiki/Contribute#net-module-development
[NET Module Versioning]: https://github.com/kraken-ng/Kraken/wiki/Contribute#net-module-versioning
[NET Module Registration]: https://github.com/kraken-ng/Kraken/wiki/Contribute#net-module-registration
[Dispatcher contributions]: https://github.com/kraken-ng/Kraken/wiki/Contribute#dispatchers
[Formater contributions]: https://github.com/kraken-ng/Kraken/wiki/Contribute#formaters
[Environment contributions]: https://github.com/kraken-ng/Kraken/wiki/Contribute#environments
[Util contributions]: https://github.com/kraken-ng/Kraken/wiki/Contribute#utils
[V. Internals]: https://github.com/kraken-ng/Kraken/wiki/Internals
[VI. FAQ & Troubleshooting]: https://github.com/kraken-ng/Kraken/wiki/FAQ-&-Troubleshooting
[Known bugs]: https://github.com/kraken-ng/Kraken/wiki/FAQ-&-Troubleshooting#known-bugs
[VII. Acknowledgments & References]: https://github.com/kraken-ng/Kraken/wiki/Acknowledgments-&-References
[Acknowledgments]: https://github.com/kraken-ng/Kraken/wiki/Acknowledgments-&-References#acknowledgments
[References]: https://github.com/kraken-ng/Kraken/wiki/Acknowledgments-&-References#references
