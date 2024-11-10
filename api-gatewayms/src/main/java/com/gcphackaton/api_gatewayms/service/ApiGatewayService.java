package com.gcphackaton.api_gatewayms.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class ApiGatewayService {

    private final RestTemplate restTemplate;

    // URL des services à partir des configurations dans application.properties
    @Value("${text-retrieval-service.url}")
    private String textRetrievalServiceUrl;

    @Value("${rhetoric-detection-service.url}")
    private String rhetoricDetectionServiceUrl;

    @Value("${response-formatter-service.url}")
    private String responseFormatterServiceUrl;

    // Constructeur
    public ApiGatewayService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    // Récupérer le texte de l'article
    public String retrieveText(String url) {
        return restTemplate.getForObject(textRetrievalServiceUrl + "?url=" + url, String.class);
    }

    // Analyser la rhétorique de l'article
    public String analyzeRhetoric(String text) {
        return restTemplate.postForObject(rhetoricDetectionServiceUrl, text, String.class);
    }

    // Formater la réponse
    public String formatResponse(String analysis) {
        return restTemplate.postForObject(responseFormatterServiceUrl, analysis, String.class);
    }
}
