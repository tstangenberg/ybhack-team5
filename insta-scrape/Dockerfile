FROM adoptopenjdk/openjdk11:latest
VOLUME /tmp
COPY insta-scrape/target/*.jar app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
