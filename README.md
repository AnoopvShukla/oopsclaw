# WhatsAppBot Core

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

## Overview

WhatsAppBot Core is a production-ready WhatsApp automation framework built with modern architectural patterns. This project provides a robust, scalable solution for building WhatsApp bots using the Baileys protocol implementation.

### Key Features

- **Modular Architecture**: Clean separation of concerns with independent service layers
- **Auto-Recovery**: Built-in connection monitoring and automatic reconnection handling
- **Credential Management**: Secure credential storage with automatic state persistence
- **Process Supervision**: Production-ready process management with automatic restarts
- **Configuration-Driven**: Environment-based configuration for easy deployment
- **Error Resilience**: Comprehensive error handling and logging throughout the stack

## Architecture

```
whatsappbot-core/
├── src/
│   ├── core/              # Core bot logic
│   ├── services/          # Service layer (messaging, auth)
│   ├── utils/             # Utility functions
│   └── config/            # Configuration management
├── scripts/
│   ├── start.sh           # Production start script
│   ├── supervise.sh       # Supervised execution
│   └── fix_credentials.py # Credential recovery utility
├── config.json            # Application configuration
└── requirements.txt       # Python dependencies
```

## Prerequisites

- Python 3.8 or higher
- Node.js 16.x or higher (for Baileys)
- Linux/Unix environment (recommended)
- 512MB RAM minimum (1GB+ recommended)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AnoopvShukla/oopsclaw.git whatsappbot-core
cd whatsappbot-core
```

### 2. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies (if using Baileys directly)
npm install
```

### 3. Configure Environment

Create your configuration in `config.json`:

```json
{
  "env_image_name": "your_environment_name",
  "supervisor_programs": [
    {
      "name": "backend",
      "command": "/path/to/backend/server",
      "directory": "/app"
    }
  ]
}
```

## Usage

### Quick Start

```bash
# Start the bot
./scripts/start.sh

# Run with supervision (auto-restart on failure)
./scripts/supervise.sh
```

### Credential Recovery

If you encounter WhatsApp registration issues:

```bash
python scripts/fix_credentials.py
```

This utility automatically fixes the Baileys `registered=false` bug by validating and correcting credential state.

## Development

### Project Structure

The codebase follows industry-standard architectural patterns:

- **Separation of Concerns**: Each module has a single, well-defined responsibility
- **Dependency Injection**: Services are loosely coupled and easily testable
- **Configuration Management**: Environment-specific settings are externalized
- **Error Boundaries**: Failures are contained and don't cascade

### Best Practices

1. **Environment Variables**: Use `.env` files for sensitive configuration
2. **Logging**: Structured logging with appropriate log levels
3. **Testing**: Unit tests for business logic, integration tests for services
4. **Documentation**: Keep inline documentation up to date
5. **Version Control**: Semantic versioning for releases

### Future-Proof Design Principles

- **Protocol Agnostic**: Easy to swap WhatsApp implementation
- **Cloud Native**: Designed for containerization and orchestration
- **Horizontal Scaling**: Stateless design allows multiple instances
- **Observability**: Built-in metrics and monitoring hooks
- **API-First**: REST/GraphQL endpoints for external integration

## Configuration

### Environment Variables

```bash
WAB_NODE_DIR=/path/to/nodejs
WAB_BOT_DIR=/path/to/bot/binary
WAB_CONFIG_PATH=/path/to/config.json
WAB_LOG_LEVEL=INFO
```

### Supervisor Configuration

The bot supports process supervision for production deployments:

- **Auto-restart**: Automatically restarts on crashes
- **Log rotation**: Prevents disk space issues
- **Status monitoring**: Real-time process health checks

## Production Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["./scripts/supervise.sh"]
```

### Systemd Service

```ini
[Unit]
Description=WhatsAppBot Core
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/opt/whatsappbot-core
ExecStart=/opt/whatsappbot-core/scripts/supervise.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### Common Issues

**Bot not connecting:**
- Check credential files in `~/.whatsappbot/credentials/`
- Verify Node.js and Python versions
- Review logs for authentication errors

**Registration errors:**
- Run `fix_credentials.py` to repair state
- Delete credential cache and re-authenticate
- Check for QR code scanning issues

**Performance issues:**
- Monitor memory usage (increase if needed)
- Check for message queue buildup
- Review database connection pool settings

## Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linters
flake8 src/
black src/
mypy src/
```

## Security

Security is a top priority. Please report vulnerabilities to security@yourdomain.com.

### Security Best Practices

- Never commit credentials to version control
- Use environment variables for sensitive data
- Regularly update dependencies
- Enable 2FA on WhatsApp accounts
- Monitor for suspicious activity

## Roadmap

### Version 2.0 (Q3 2026)
- [ ] Multi-account support
- [ ] GraphQL API
- [ ] Advanced analytics dashboard
- [ ] Plugin system for extensions

### Version 3.0 (Q1 2027)
- [ ] Kubernetes operator
- [ ] Multi-protocol support (Telegram, Signal)
- [ ] AI-powered response system
- [ ] Enterprise SSO integration

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Baileys](https://github.com/adiwajshing/Baileys) - WhatsApp Web API implementation
- The open-source community for inspiration and support

## Support

For support, please:
- Open an issue on GitHub
- Check the [documentation](https://github.com/AnoopvShukla/oopsclaw/wiki)
- Join our community Discord server

## Contact

Maintainer: [AnoopvShukla](https://github.com/AnoopvShukla)

---

**Built with ❤️ for the automation community**
