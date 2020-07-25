import pgc from "@textile/powergate-client"
import rpc_ab from "@textile/grpc-powergate-client/dist/ffs/rpc/rpc_pb.js"
import fs from "fs"

const { JobStatus } = rpc_ab
const { createPow } = pgc;

// example: node pow.js file/path 
let args = {}
process.argv.forEach(function (val, index, array) {
    args[index] = val
    console.log('args: ' + index + ': ' + val);
});
let filepath = args[2]

const host = "http://0.0.0.0:6002" // or whatever powergate instance you want

const pow = createPow({ host })
main(filepath)
// const token = makeToken()
// // await pow.setToken(token)
// store_file_ffs(filepath)

// async function setToken(to) {
//     const token
// }

async function main(filepath) {
  const token = await makeToken()
  store_file_ffs(filepath)
}

async function makeToken() {
  const { token } = await pow.ffs.create() // save this token for later use!
  console.log('token:', token)
  pow.setToken(token)
  return token
}


// copied from https://github.com/textileio/js-powergate-client
async function store_file_ffs(filepath) {
    // get wallet addresses associated with your FFS instance
    const { addrsList } = await pow.ffs.addrs()
  
    // create a new address associated with your ffs instance
    const { addr } = await pow.ffs.newAddr("my new addr")
  
    // get general info about your ffs instance
    const { info } = await pow.ffs.info()
  
    console.log("debug: ", info, addr, addrsList)

    // cache data in IPFS in preparation to store it using FFS
    const buffer = fs.readFileSync(filepath)
    const { cid } = await pow.ffs.addToHot(buffer)
  
    // store the data in FFS using the default storage configuration
    const { jobId } = await pow.ffs.pushConfig(cid)
  
    // watch the FFS job status to see the storage process progressing
    const jobsCancel = pow.ffs.watchJobs((job) => {
      if (job.status === JobStatus.JOB_STATUS_CANCELED) {
        console.log("job canceled")
        return
        
      } else if (job.status === JobStatus.JOB_STATUS_FAILED) {
        console.log("job failed")
      } else if (job.status === JobStatus.JOB_STATUS_SUCCESS) {
        console.log("job success!")
      }
    }, jobId)
  
    // watch all FFS events for a cid
    const logsCancel = pow.ffs.watchLogs((logEvent) => {
      console.log(`received event for cid ${logEvent.cid}`)
    }, cid)
  
    // get the current desired storage configuration for a cid (this configuration may not be realized yet)
    // const { config } = await pow.ffs.getStorageConfig(cid)
  
    // // get the current actual storage configuration for a cid
    // const { cidInfo } = await pow.ffs.show(cid)
  
    // // retrieve data from FFS by cid
    // const bytes = await pow.ffs.get(cid)
  
  }