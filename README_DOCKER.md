# 🐳 Docker Deployment Guide

## Quick Start

```bash
# Build and run the games collection
docker-compose up --build

# Access at http://localhost:8080
```

## Production Deployment

### 1. Server Setup
```bash
# Clone the repository
git clone https://github.com/helvard/nanna_spil.git
cd nanna_spil

# Configure your domain in docker-compose.yml
# Replace 'your-domain.com' with your actual domain
```

### 2. SSL with Traefik
```bash
# Run with automatic SSL
docker-compose up -d

# Traefik will automatically get SSL certificates from Let's Encrypt
```

### 3. Manual Deployment (Simple)
```bash
# Build only the web service
docker build -t nanna-spil .
docker run -p 8080:80 nanna-spil
```

## Configuration

### Environment Variables
- `NODE_ENV=production` - Production mode
- Domain configuration in `docker-compose.yml`

### Port Configuration
- Default: `8080:80`
- Change in `docker-compose.yml` ports section

## File Structure After Deployment

```
/usr/share/nginx/html/
├── index.html                 # Main game collection page
├── Games/
│   ├── Bogstaver/
│   │   └── Bogstavjagt/
│   │       └── bogstavjagt_arcade.py
│   └── Vendespil/
│       └── vendespil_ipad.html
├── paw_patrol/               # Game assets
├── stave_navn_improved.html
└── kalaha.html
```

## Monitoring

### Health Check
```bash
# Check container health
docker-compose ps

# View logs
docker-compose logs -f
```

### Performance
- Nginx serves static files efficiently
- Gzip compression enabled
- Browser caching configured
- SSL termination

## Security

- Security headers configured
- No server-side code execution
- Static file serving only
- Rate limiting recommended

## Customization

### Adding New Games
1. Add game files to appropriate `Games/` subfolder
2. Update `index.html` to include the new game
3. Rebuild: `docker-compose up --build`

### Custom Domain
Update `docker-compose.yml`:
```yaml
labels:
  - "traefik.http.routers.nanna-spil.rule=Host(`your-new-domain.com`)"
```

## Troubleshooting

### Port Issues
```bash
# Check what's using port 8080
lsof -i :8080

# Kill process if needed
kill -9 <PID>
```

### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod -R 755 Games/
```

### SSL Issues
- Ensure domain DNS points to server
- Check Let's Encrypt rate limits
- Verify port 80/443 accessibility

## Backup

```bash
# Backup game files
tar -czf nanna-spil-backup.tar.gz Games/ paw_patrol/ *.html

# Restore
tar -xzf nanna-spil-backup.tar.gz
```

## Scaling

For high traffic:
```yaml
# In docker-compose.yml
services:
  nanna-spil:
    deploy:
      replicas: 3
```

## Support

- Check logs: `docker-compose logs`
- Health check: `curl http://localhost:8080`
- Issues: GitHub repository
