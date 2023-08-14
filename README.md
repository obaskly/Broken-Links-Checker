# 🌐 Broken Links Checker

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Issues](https://img.shields.io/github/issues-raw/your-username/repository-name)

A Python-based tool designed to efficiently identify broken links on a given website. With concurrent requests and the integration of Selenium, ensure that you're providing the best user experience by keeping all your links in check.

<p align="center">
    <img src="path-to-screenshot-or-gif" width="600" alt="Broken Links Checker Screenshot/GIF">
</p>

## 🚀 Features

- **Proxy Support**: Seamlessly fetches and utilizes proxies for accurate link validation.
- **User-Agent Rotation**: Simulates various devices and browsers.
- **Selenium**: Deep link inspections, especially when handling challenges like Cloudflare.
- **Fast**: Concurrent requests via multi-threading.

## 📋 Prerequisites

- Python (3.6 or higher)
- ChromeDriver (for Selenium)
- Required Python libraries:
  ```
  pip install selenium fake_useragent tqdm colorama cloudscraper requests
  ```

## 🎈 Usage

1. **Clone and navigate**:
   ```
   git clone https://github.com/obaskly/Broken-Links-Checker.git
   cd Broken-Links-Checker
   ```

2. **Execute the script**:
   ```
   python main.py
   ```

3. **Follow the on-screen instructions**:
   - Submit your website's URL.
   - Determine the number of proxies to fetch.

4. **Results**:
   - The script will filter working proxies.
   - The script will list any broken links discovered.

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## 📜 License

This project is licensed under the MIT License.

## 🌟 Acknowledgements

- [Selenium](https://www.selenium.dev/)
- [fake_useragent](https://pypi.org/project/fake-useragent/)
- [cloudscraper](https://github.com/VeNoMouS/cloudscraper)
- And other libraries used in the project.
