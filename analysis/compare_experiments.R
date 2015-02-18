library(data.table)
library(ggplot2)
library(lubridate)

if (FALSE) {
    exps.raw = as.data.table(do.call(rbind, lapply(list.files("runs", full.names=TRUE), function(f) {
        d = read.delim(f, col.names=c("strength", "address", "type", "subtype",
                                      "datetime", "fcs"), sep="\t")
        d$experiment = gsub(".txt", "", f)
        d
    })))
}

exps = exps.raw[address != ""]
exps = exps[!is.na(strength)]

# parse dates

interesting = read.csv("interesting.txt", header=FALSE, col.names=c("name", "address"), sep="\t")
exps = merge(exps, interesting, by="address", all.x=TRUE)

exps = exps[is.na(name) | name != "Dan's Laptop"]

exps$datetime = lubridate::parse_date_time(exps$datetime, "mdyhms", tz="EST")

exps2 = exps[grepl("exp2", experiment)]

summarize.dat = function(dat, by) {
    dat[, list(number=length(strength), strength=median(strength, na.rm=T) + 0, strengthSD=sd(strength), interesting=sum(!is.na(name))), by=by][order(number)]
}

addr.summary = summarize.dat(exps, by=c("address", "type", "subtype"))
multitypes = addr.summary[, list(numtype=length(type)), by="address"][numtype > 1][order(numtype)]
addr.summary[address %in% multitypes$address]

subtype.summary = summarize.dat(exps, by=c("experiment", "type", "subtype"))
interesting.summary = summarize.dat(exps[!is.na(name)], by=c("name", "experiment", "type", "subtype"))

shared = exps2[order(experiment)][, list(number=length(strength), strength=paste(strength, collapse=","), sources=length(unique(experiment)), strength1=strength[1], strength2=strength[2], t1=datetime[1], t2=datetime[2]), by=c("address", "type", "subtype", "fcs")]
packets2 = shared[sources == 2 & number == 2]

print(ggplot(packets2, aes(strength1, strength2)) + geom_point())

print(ggplot(exps2[type == 0 & subtype == 4], aes(strength)) + geom_histogram() + facet_wrap(~ experiment))

addr.summary = summarize.dat(exps, by=c("address", "type", "subtype", "experiment"))

# combine with companies
companies = read.csv("../codes/codes.csv", col.names=c("prefix", "company"), header=FALSE)

exps$prefix = substr(exps$address, 1, 8)
exps = merge(exps, companies, by="prefix", all.x=TRUE)

has.company = droplevels(exps[!is.na(company)])
sort(table(has.company$company))

# summarize by address noise

byaddrs = summarize.dat(exps, by=c("experiment", "address"))[number > 1]

ggplot(byaddrs, aes(number, strengthSD, col=strength)) + geom_point() + scale_x_log10() + facet_wrap(~ experiment)


