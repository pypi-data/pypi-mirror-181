
### step class ###

step class consist common  functions which can be inherited by other classes  -- setTaskID, setUUID,setTaskExecutionID,startRedisConn,setLogger,loadParams,connectToAPIForKey,createAndGetResponseFromURL,getLogger,exceptionTraceback,getRelativeFile;

### extract class###

extract class consist of init method which sets all loadParams and log files .. also contains super class startup which can be defined from client extract ..  it also consist of startWs- starting websocket connection functions .;

### ML class ###

Ml class consist of startup method ,startMLSubscriber to subscribr to the incoming data ,process ml to process data   , compute ml   to do client ML computations and handoff it to  next step;


### Transform class ###

Transform class consist of startup  ,startTRSubscriber to subscribr to the incoming data , tranformExData -function has to be defined inside clientTranform with own tranform logic .It also consist of microBatchProcessRedisSortedSet  for microbatching    streaming data ./;


### Load Class ###

Load class consist of startup method , loadsubscribers to listen to the data and  client logic to  loading final data needs to be added in client load file;

### New Release Note version='0.1.20' ###

Rebuilt from master. with  relativefileLocation changes , Step class logger issue fixed

Rebuilt from master ,with LogMessageFormate changes , in Step Class issue fixed