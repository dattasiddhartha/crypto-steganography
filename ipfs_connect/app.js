
const express = require('express')
const app = express()
const port = 2999
const util = require('util');
const exec = util.promisify(require('child_process').exec);
const path = require('path');
const fs = require('fs')
const multer = require("multer");

const tmppath = './tmp/'
const file_store_path = "../data"
const pycli = 'python ../run_cli.py';

app.use(express.json())

app.get('/', (req, res) => res.send('Hello World!'))

// python cli
app.post('/py/store', (req, res) => {
  // shell out to py cli to mask image
  // python run_cli.py --function store --filename cyclegan_test --style_index 1

  // Debug:
  // console.log(req, res)
  // console.log(req.body)
  // console.log('---')

  let { filename, styleindex } = req.body;
  filename = filename ? filename.toString() : 'cyclegan_test';
  styleindex = styleindex ? styleindex.toString() : '1';

  async_call_pycli('store', filename, styleindex, res);
})

app.post('/py/restore', (req, res) => {
  // shell out to py cli to restore image
  // python run_cli.py --function restore --filename cyclegan_test --style_index 1
  let { filename, styleindex } = req.body;
  filename = filename ? filename.toString() : 'cyclegan_test';
  styleindex = styleindex ? styleindex.toString() : '1';

  async_call_pycli('restore', filename, styleindex, res);
})


// file upload
const handleError = (err, res) => {
  res
    .status(500)
    .contentType("text/plain")
    .end("Oops! Something went wrong!");
};

const upload = multer({
  dest: tmppath
  // you might also want to set some limits: https://github.com/expressjs/multer#limits
});

app.post(
  "/upload",
  upload.single("file" /* name attribute of <file> element in your form */),
  (req, res) => {
    const tempPath = req.file.path;
    const originalname = req.file.originalname;
    const targetPath = path.join(__dirname, file_store_path, originalname);
    console.log("file uploaded to: ", targetPath, tempPath, req.file)

    fs.rename(tempPath, targetPath, err => {
      if (err) return handleError(err, res);

      res
        .status(200)
        .contentType("text/plain")
        .end("File uploaded!");
    });
  }
);

app.use("/fileupload", express.static(path.join(__dirname, "./public/index.html")));

async function async_call_pycli(func, filename, styleindex, res) {
  let cmd = `${pycli} --function ${func} --filename ${filename} --style_index ${styleindex}`;
  console.log(`Executing shell cmd: ${cmd}`)
  const { stdout, stderr } = await exec(cmd);
  console.log('stdout:', stdout);
  console.error('stderr:', stderr);
  if (stderr.length > 0) {
    handleError(stderr, res)
  }
  res.status(200).contentType("text/plain").end(stdout);
}

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))
