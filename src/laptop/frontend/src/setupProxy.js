const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
    app.use(createProxyMiddleware('/image',
        { target: 'http://localhost:5000/' }
    ));
}
