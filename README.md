# api_lotus

For api i used flask + sqlalchemy(postgres). 

To pull from dockerhub write this command in console:
 - sudo docker pull 22051507/lotus_flare_test:latest

To run:
 - sudo docker-compose run -d migration
 
Endpoints:
1) average_time?date=2019-10-18. Whete date - parameter. Date format "Y-m-d"
2) rows_per_thread?time_start=2019-10-18&time_end=2019-10-19. Time_start, time_end in formats: "Y-m-d/H:M:S", "Y-m-d/H:M", "Y-m-d"
2) rows_per_second?time_start=2019-10-18&time_end=2019-10-19. Time_start, time_end in formats: "Y-m-d/H:M:S", "Y-m-d/H:M", "Y-m-d"
2) threads_per_second?time_start=2019-10-18&time_end=2019-10-19. Time_start, time_end in formats: "Y-m-d/H:M:S", "Y-m-d/H:M", "Y-m-d"

Estimated time to execute:
 - 0.076 +- 0.02 seconds
