library(data.table)
library(ggplot2)

exps.raw = as.data.table(do.call(rbind, lapply(list.files("runs", full.names=TRUE), function(f) {
    d = read.delim(f, col.names=c("strength", "address", "type", "subtype",
                                  "datetime", "fcs"), sep="\t")
    d$experiment = gsub(".txt", "", f)
    d
})))

exps = exps.raw[address != ""]
exps = exps[!is.na(strength)]

interesting = read.csv("interesting.txt", header=FALSE, col.names=c("name", "address"), sep="\t")
exps = merge(exps, interesting, by="address", all.x=TRUE)

summarize.dat = function(dat, by) {
    dat[, list(number=length(address), strength=median(strength, na.rm=T) + 0,
                interesting=sum(!is.na(name))), by=by][order(number)]
}

addr.summary = summarize.dat(exps, by=c("address"))
subtype.summary = summarize.dat(exps, by=c("experiment", "type", "subtype"))
interesting.summary = summarize.dat(exps[!is.na(name)], by=c("name", "experiment", "type", "subtype"))

