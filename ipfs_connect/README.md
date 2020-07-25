# Uploading to ipfs

# Via powergate
1. image upload
   1. set up powergate https://gist.github.com/andrewxhill/b0010d555ca4d79d9d1e78e380ad218e#file-index-md  
   2. ```
        pow ffs create
        export POW_TOKEN=<token value from above>
        pow ffs addToHot ./crypto-steganography/data/mask.png 
        pow ffs push --watch <cid from ^>
      ```
2. image retrieval
   1. `pow ffs get <cid> <filename>`

# via powergate js cli
Make sure you install the deps by cd-ing in and running `npm i`.   
`node js/cli/pow.js filepath`  

# server quickstart
```
npm i
node app.js
```

# server routes
2 routes for py cli store and restore.   
- http://localhost:2999/py/store
- http://localhost:2999/py/store
example: 
`curl -i -X POST -H 'Content-Type: application/json' -d '{"filename": "path"}' --url 'http://localhost:2999/py/store'`
You can also pass in a custom styleindex, defaults to 1. 

file upload
  - static test page: http://localhost:2999/fileupload
  - file upload post route: http://localhost:2999/upload
