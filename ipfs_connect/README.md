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

