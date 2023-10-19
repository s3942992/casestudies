library(ggplot2)
library(xlsx)
library(dplyr)
library(plotly)
library(tidyr)
library(cowplot)
library(reshape2)
library(car)
library(GGally)

# Load your data
data <- read.xlsx("datasetone_1697404795.xlsx", sheetName = "datasetone", rowIndex = 3:1721, colIndex = 1:7)
data$AreaHa <- as.numeric(data$AreaHa)
data$Shape__Length <- as.numeric(data$Shape__Length)
data$Shape__Area <- as.numeric(data$Shape__Area)
data$PerimeterM <- as.numeric(data$PerimeterM)
data$AreaHa <- round(data$AreaHa, 2)
data$PerimeterM <- round(data$PerimeterM, 2)
data$Shape__Area <- round(data$Shape__Area, 2)
data$Shape__Length <- round(data$Shape__Length, 2)




average_area_by_year <- data %>%
    gather(Variable, Average_Area, PerimeterM, Shape__Area, Shape__Length, AreaHa) %>%
    group_by(Year, Variable) %>%
    summarize(Average_Area = mean(Average_Area, na.rm = TRUE))

# Create a facetted time series plot
time_series_plot <- ggplot(average_area_by_year, aes(x = Year, y = Average_Area, color = Variable)) +
    geom_line() +
    labs(
        title = "                                                      Space consumed each year",
        x = "Year",
        y = "Spaces taken up(refer to variables)"
    ) +
    facet_wrap(~Variable, scales = "free_y")

# Show the facetted plot
print(time_series_plot)


summary(data)



correlation_matrix <- cor(data[, c('AreaHa', 'PerimeterM', 'Shape__Area', 'Shape__Length')])
# Create a ggplot2 heatmap of the correlation matrix
ggplot(data = melt(correlation_matrix), aes(Var1, Var2, fill = value)) +
    geom_tile() +
    scale_fill_gradient(low = "blue", high = "red") +
    theme_minimal() +
    labs(title = "                                                                  Correlation Heatmap")

remove_outliers <- function(column) {
    Q1 <- quantile(column, 0.25, na.rm = TRUE)
    Q3 <- quantile(column, 0.75, na.rm = TRUE)
    IQR_value <- Q3 - Q1
    lower_bound <- Q1 - 3 * IQR_value
    upper_bound <- Q3 + 3 * IQR_value
    column[column < lower_bound | column > upper_bound] <- NA
    return(column)
}

# Apply the function to each numeric column in the dataset
numeric_columns <- sapply(data, is.numeric)
data[numeric_columns] <- lapply(data[numeric_columns], remove_outliers)

# Remove rows with missing values
data <- na.omit(data)

# Create boxplots of the modified data
par(mfrow = c(2, 2))
boxplot(data$AreaHa, main = "Boxplot of AreaHa")
boxplot(data$PerimeterM, main = "Boxplot of PerimeterM")
boxplot(data$Shape__Area, main = "Boxplot of Shape__Area")
boxplot(data$Shape__Length, main = "Boxplot of Shape__Length")
par(mfrow = c(1, 1))





##########################################


pairs(numericcol)
ggpairs(numericcol)
