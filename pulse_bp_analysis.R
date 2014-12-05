library(stringr)
library(dplyr)
library(reshape2)
participant_files <- list.files(pattern = '*.txt')

colnames <- c('time', 'orgi_trial', 'adv', 'mksh', 'revg', 'price_d',
            'price_r', 'estm_orig', 'time_r',
            'participant_response', 'condition_number',
            'bp_s', 'bp_d', 'pulse')

participant_file <- "A43538908_A43538908.txt"

file_to_long <- function(participant_file){
    values <- c()
    print(participant_file)
    df <- read.table(participant_file, header = FALSE, sep = ",",
                     col.names = colnames,
                     fill = TRUE, stringsAsFactors = FALSE)
    length(df$time)

    # assign sections
    # there are 15 trials for each section
    # there are 12 sections for a total of 180 responess
    sections <- c()
    for(j in 1:12){
        sections <- c(sections, rep(j, 15))
    }
    df$section <- sections

    # clean response data
    df$participant_response[df$participant_response == "" | is.na(df$participant_response)] <- NA
    df$participant_response <- as.numeric(df$participant_response)
    df$abs_diff <- abs(df$price_r - df$participant_response)

    df_section_summary <- df %>%
        group_by(section) %>%
        summarize(avg_difference = mean(abs_diff, na.rm = TRUE,),
                  num_responses = n())

    df_subset <- df[, c('section', 'condition_number', 'bp_s', 'bp_d', 'pulse')]
    df_section_summary  <- merge(x = na.omit(df_subset),
                                 y = df_section_summary,
                                 by = 'section', all.y = TRUE)

    df_section_summary$respondent <- participant_file
    df_section_summary$section <- as.character(df_section_summary$section)

    avg_diff_vector <- df_section_summary[1:12, "avg_difference"]
    num_respons_vector <- df_section_summary[1:12, "num_responses"]

    avg_times_number <- avg_diff_vector * num_respons_vector
    sum_avg_times_number <- sum(avg_times_number)
    total_num_responses <- sum(num_respons_vector)
    test_average_difference <- sum_avg_times_number / total_num_responses

    avg_bp_s <- mean(df_section_summary$bp_s, na.rm = TRUE)
    avg_bp_d <- mean(df_section_summary$bp_d, na.rm = TRUE)
    avg_pulse <- mean(df_section_summary$pulse, na.rm = TRUE)
    condition_number <- unique(na.omit(df_section_summary$condition_number))
    values <- c('Total_avg_diff', condition_number, avg_bp_s, avg_bp_d, avg_pulse,
                test_average_difference, total_num_responses, participant_file)

    df_section_summary <- rbind(df_section_summary, values)

    long <- df_section_summary[!is.na(df_section_summary$section), ]
    print(long)
    return(long)
}

temp_long <- file_to_long(participant_file)

dataframe <- temp_long

long_to_wide <- function(dataframe){
    respondent <- unique(na.omit(dataframe$respondent))
    respondent

    condition_number <- unique(na.omit(dataframe$condition_number))
    condition_number

    values_wide <- c(respondent, condition_number)
    values_wide

    values_names <- c("respondent", "condition_number")
    values_names

    k <- 1
    l <- 3

    for(k in 1:length(dataframe$section)){
        for(l in 3:length(names(dataframe))- 1){
            new_column_name <- paste(names(dataframe)[l], dataframe$section[k], sep = "_")
            new_column_name
            values_names <- c(values_names, new_column_name)
            values_names

            new_value <- dataframe[k, l]
            new_value

            values_wide <- c(values_wide, new_value)
            values_wide
        }
    }
    values_wide <- t(as.matrix(values_wide))
    values_wide <- as.data.frame(values_wide)
    names(values_wide) <- values_names
    return(values_wide)
}

long_to_wide(temp_long)

##############################################################################

all_long <- data.frame()
all_wide <- data.frame()

for(participant_file in participant_files){
    long <- file_to_long(participant_file)
    wide <- long_to_wide(long)

    all_long <- rbind(all_long, long)
    all_wide <- rbind(all_wide, wide)
}

write.csv(all_long, 'all_long.csv', row.names = FALSE)
write.csv(all_wide, 'all_wide.csv', row.names = FALSE)
