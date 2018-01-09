ilp_data = read.csv("ilp_result.txt", header=FALSE)
brkga_data = read.csv("brkga_result.txt", header=FALSE)
grasp_data = read.csv("grasp_result.txt", header=FALSE)

min_common_size = min(nrow(ilp_data), nrow(brkga_data), nrow(grasp_data))

# Compare ilp, brkga and grasp
sub_ilp = head(ilp_data, min_common_size)
sub_brkga = head(brkga_data, min_common_size)
sub_grasp = head(grasp_data, min_common_size)

# Compare time
time_table = data.frame(level=sub_ilp[1], ilp=as.numeric(unlist(sub_ilp[3])), brkga=as.numeric(unlist(sub_brkga[3])), grasp=as.numeric(unlist(sub_grasp[3])) )
time_table[1] = gsub("^[^_]*_|_[^_]*$", "", as.matrix(time_table[1]))
time_table[1] = as.numeric(as.matrix(time_table[1]))
time_table = aggregate(. ~ V1, time_table, FUN=mean)

# define 3 data sets
xdata <- as.matrix(time_table[1])
y1 <- as.matrix(time_table[2])
y2 <- as.matrix(time_table[3])
y3 <- as.matrix(time_table[4])

# plot the first curve by calling plot() function
# First curve is plotted
plot(xdata, y1, type="o", col="blue", pch="o", lty=1, ylim=range(y1,y2,y3), ylab="CPU time (second)", xlab = "Problem size (hours)" )

points(xdata, y2, col="red", pch="*")
lines(xdata, y2, col="red",lty=2)

points(xdata, y3, col="green",pch="+")
lines(xdata, y3, col="green", lty=3)

legend(x= "topleft", y=0.92,legend=c("ilp","brkga","grasp"), col=c("blue","red","green"),
       pch=c("o","*","+"),lty=c(1,2,3), ncol=1)

# Compare objective value
obj_table = data.frame(level=sub_ilp[1], ilp=as.numeric(unlist(sub_ilp[2])), brkga=as.numeric(unlist(sub_brkga[2])), grasp=as.numeric(unlist(sub_grasp[2])) )
obj_table[1] = gsub("^[^_]*_|_[^_]*$", "", as.matrix(obj_table[1]))
obj_table[1] = as.numeric(as.matrix(obj_table[1]))
obj_table = aggregate(. ~ V1, obj_table, FUN=mean)

# define 3 data sets
xdata <- as.matrix(obj_table[1])
y1 <- as.matrix(obj_table[2])
y2 <- as.matrix(obj_table[3])
y3 <- as.matrix(obj_table[4])

# plot the first curve by calling plot() function
# First curve is plotted
plot(xdata, y1, type="o", col="blue", pch="o", lty=1, ylim=range(y1,y2,y3), ylab="Objective value (nurse)", xlab = "Problem size (hours)" )

points(xdata, y2, col="red", pch="*")
lines(xdata, y2, col="red",lty=2)

points(xdata, y3, col="green",pch="+")
lines(xdata, y3, col="green", lty=3)

legend(x= "topleft", y=0.92,legend=c("ilp","brkga","grasp"), col=c("blue","red","green"),
       pch=c("o","*","+"),lty=c(1,2,3), ncol=1)


# Compare brkga and grasp
min_common_size = min(nrow(brkga_data), nrow(grasp_data))
sub_brkga = head(brkga_data, min_common_size)
sub_grasp = head(grasp_data, min_common_size)

# Compare time
time_table = data.frame(level=sub_brkga[1], brkga=as.numeric(unlist(sub_brkga[3])), grasp=as.numeric(unlist(sub_grasp[3])) )
time_table[1] = gsub("^[^_]*_|_[^_]*$", "", as.matrix(time_table[1]))
time_table[1] = as.numeric(as.matrix(time_table[1]))
time_table = aggregate(. ~ V1, time_table, FUN=mean)

# define 3 data sets
xdata <- as.matrix(time_table[1])
y1 <- as.matrix(time_table[2])
y2 <- as.matrix(time_table[3])

# plot the first curve by calling plot() function
# First curve is plotted
plot(xdata, y1, type="o", col="red", pch="*", lty=1, ylim=range(y1,y2), ylab="CPU time (second)", xlab = "Problem size (hours)" )

points(xdata, y2, col="green", pch="+")
lines(xdata, y2, col="green",lty=2)

legend(x= "topleft", y=0.92,legend=c("brkga","grasp"), col=c("red","green"),
       pch=c("o","+"),lty=c(1,2), ncol=1)


# Compare time
obj_table = data.frame(level=sub_brkga[1], brkga=as.numeric(unlist(sub_brkga[2])), grasp=as.numeric(unlist(sub_grasp[2])) )
obj_table[1] = gsub("^[^_]*_|_[^_]*$", "", as.matrix(obj_table[1]))
obj_table[1] = as.numeric(as.matrix(obj_table[1]))
obj_table = aggregate(. ~ V1, obj_table, FUN=mean)

# define 3 data sets
xdata <- as.matrix(obj_table[1])
y1 <- as.matrix(obj_table[2])
y2 <- as.matrix(obj_table[3])

# plot the first curve by calling plot() function
# First curve is plotted
plot(xdata, y1, type="o", col="red", pch="*", lty=1, ylim=range(y1,y2), ylab="Objective value (nurse)", xlab = "Problem size (hours)" )

points(xdata, y2, col="green", pch="+")
lines(xdata, y2, col="green",lty=2)

legend(x= "topleft", y=0.92,legend=c("brkga","grasp"), col=c("red","green"),
       pch=c("o","+"),lty=c(1,2), ncol=1)
