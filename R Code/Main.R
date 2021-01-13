library(plspm)

generalUserStats = read.csv(sprintf("../userStats.csv"), header=TRUE, sep=";", stringsAsFactors = TRUE)
generalUserStats$QuestionRatio =generalUserStats$CorrectCount / generalUserStats$QuestionCount

generalUserStats$MI = generalUserStats$miacI + generalUserStats$micoI + generalUserStats$mistI
generalUserStats$ME = generalUserStats$meidI + generalUserStats$meinI + generalUserStats$mereI
generalUserStats$MIVar = generalUserStats$miacVar + generalUserStats$micoVar + generalUserStats$mistVar
generalUserStats$MEVar = generalUserStats$meidVar + generalUserStats$meinVar + generalUserStats$mereVar


# Hexad PLS

ludimoodlePath = rbind(
  c(0,0,0,0,0,0,0,0,0),
  c(0,0,0,0,0,0,0,0,0),
  c(0,0,0,0,0,0,0,0,0),
  c(0,0,0,0,0,0,0,0,0),
  c(0,0,0,0,0,0,0,0,0),
  c(0,0,0,0,0,0,0,0,0),
  c(1,1,1,1,1,1,0,0,0),
  c(1,1,1,1,1,1,0,0,0),
  c(1,1,1,1,1,1,0,0,0)
)

colnames(ludimoodlePath) = rownames(ludimoodlePath) = c("achiever","player","socialiser","freeSpirit","disruptor","philanthropist","MIVar","MEVar","amotVar")

ludimoodleblocks = as.list(which( colnames(generalUserStats)%in%colnames(ludimoodlePath) ))

ludiModes = c("A", "A", "A", "A", "A", "A", "A", "A", "A")

gameElements = levels(generalUserStats$GameElement)

for (gameElement in gameElements){
  sub = subset(generalUserStats, GameElement==gameElement)
  
  plsRes = plspm(sub, ludimoodlePath, ludimoodleblocks, modes = ludiModes, boot.val=T, br=200)
  pathCoefs = plsRes$path_coefs[c("MIVar", "MEVar", "amotVar"), c("achiever","player","socialiser","freeSpirit","disruptor","philanthropist")]
  pVals = cbind(
    plsRes$inner_model$MIVar[2:7,4],
    plsRes$inner_model$MEVar[2:7,4],
    plsRes$inner_model$amotVar[2:7,4]
  )
  
  colnames(pVals) = c("MIVar", "MEVar", "AMOTVar")
  
  pVals = t(pVals)
  
  write.table(pathCoefs, sprintf("PLS/Hexad/%sPathCoefs.csv",gameElement), sep=";", col.names=NA)
  write.table(pVals, sprintf("PLS/Hexad/%spVals.csv", gameElement), sep=";", col.names=NA)
}


ludimoodlePath = rbind(
  c(0,0,0,0,0,0),
  c(0,0,0,0,0,0),
  c(0,0,0,0,0,0),
  c(1,1,1,0,0,0),
  c(1,1,1,0,0,0),
  c(1,1,1,0,0,0)
)

colnames(ludimoodlePath) = rownames(ludimoodlePath) = c("MI", "ME","amotI","MIVar","MEVar","amotVar")

ludimoodleblocks = as.list(which( colnames(generalUserStats)%in%colnames(ludimoodlePath) ))

ludiModes = c("A", "A", "A", "A", "A", "A")

gameElements = levels(generalUserStats$GameElement)

for (gameElement in gameElements){
  sub = subset(generalUserStats, GameElement==gameElement)
  
  plsRes = plspm(sub, ludimoodlePath, ludimoodleblocks, modes = ludiModes, boot.val=T, br=200)
  pathCoefs = plsRes$path_coefs[c("MIVar", "MEVar", "amotVar"), c("MI", "ME","amotI")]
  pVals = cbind(
    plsRes$inner_model$MIVar[2:4,4],
    plsRes$inner_model$MEVar[2:4,4],
    plsRes$inner_model$amotVar[2:4,4]
  )
  
  colnames(pVals) = c("MIVar", "MEVar", "AMOTVar")
  
  pVals = t(pVals)
  
  write.table(pathCoefs, sprintf("PLS/Motivation/%sPathCoefs.csv",gameElement), sep=";", col.names=NA)
  write.table(pVals, sprintf("PLS/Motivation/%spVals.csv", gameElement), sep=";", col.names=NA)
}

