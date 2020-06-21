const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
    app.use(createProxyMiddleware('/image',
        { target: 'http://localhost:5000/' }
    ));
    app.use(createProxyMiddleware('/allData',
        { target: 'http://localhost:5000/' }
    ));
    app.use(createProxyMiddleware('/specificData',
        { target: 'http://localhost:5000/' }
    ));
}
