library(stringr)
library(dplyr)
library(reshape2)
participant_files <- list.files(pattern = '*.txt')

colnames <- c('time', 'orgi_trial', 'adv', 'mksh', 'revg', 'price_d',
            'price_r', 'estm_orig', 'time_r',
            'participant_response', 'condition_number',
            'bp_s', 'bp_d', 'pulse')

all <- data.frame()

# i <- 1
for(i in 1:length(participant_files)){
    print(participant_files[i])
    df <- read.table(participant_files[i], header = FALSE, sep = ",",
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
    df[df$participant_response == "", ] <- NA
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

    df_section_summary$respondent <- participant_files[i]
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
                test_average_difference, total_num_responses, participant_files[i])

    df_section_summary <- rbind(df_section_summary, values)

    df_section_summary <- na.omit(df_section_summary)

    all <- rbind(all, df_section_summary)
}

write.csv(all, 'all.csv', row.names = FALSE)


# transpose <- as.matrix(df_section_summary) %>% t() %>% as.data.frame()

# dcast(df_section_summary, bp_s + b p_d + pulse + avg_difference + num_responses ~ respondent)

# string <- "120\033[A\033[A"
# pattern <- '\\\\[:digit:]{1, }\\[[:alpha:]*'
# pattern <- '\\\\'
# str_replace_all(string = string, pattern = pattern, replacement = "")

