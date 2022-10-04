const http = require('http')

//const hostname = '127.0.0.1'
const hostname = '0.0.0.0'
//const port = process.env.PORT
const port = 8080

const server = http.createServer((req, res) => {
  res.statusCode = 200
  res.setHeader('Content-Type', 'text/plain')
  res.end('Hello World!\n')
  console.log(`Request!`)
})

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`)
})