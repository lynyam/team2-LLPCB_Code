package com.gcphackaton.api_gatewayms.service;

import org.jsoup.nodes.Element;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import java.net.*;
import java.io.*;
import org.json.JSONObject;

import java.util.Arrays;

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

        //return restTemplate.getForObject(textRetrievalServiceUrl + "?url=" + url, String.class);
        StringBuilder content = new StringBuilder();

        try {
            // Se connecter à l'URL et récupérer le document HTML
            Document document = Jsoup.connect(url).get();
            // Extraction du texte uniquement
            String textOnly = document.text();
            String[] sentences = textOnly.split("\\."); // Séparer par les points
            for (String sentence : sentences) {
                System.out.println(sentence.trim() + "."); // Afficher chaque phrase avec un retour à la ligne
            }
            System.out.println("\n\n=====================================\n\n");

            return textOnly;

        } catch (Exception e) {
            e.printStackTrace();
            return "Erreur lors de la récupération du texte : " + e.getMessage();
        }
    }

    // Analyser la rhétorique de l'article
    private static final String PYTHON_API_URL = "http://localhost:8081/analyze";
    public JSONObject analyzeRhetoric(String text) throws IOException {
        // Créer la connexion HTTP
        URL url = new URL(PYTHON_API_URL);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/json");
        connection.setDoOutput(true);

        // Créer le corps de la requête JSON
        JSONObject requestPayload = new JSONObject();
        requestPayload.put("text", text);

        // Envoyer la requête
        try (OutputStream os = connection.getOutputStream()) {
            byte[] input = requestPayload.toString().getBytes("utf-8");
            os.write(input, 0, input.length);
        }

        // Lire la réponse
        int responseCode = connection.getResponseCode();
        if (responseCode != HttpURLConnection.HTTP_OK) {
            throw new IOException("HTTP request failed with code " + responseCode);
        }

        try (BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream(), "utf-8"))) {
            StringBuilder response = new StringBuilder();
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }
            JSONObject jsonResponse = new JSONObject(response.toString());

            // Afficher le JSON dans un format lisible
            System.out.println(jsonResponse.toString(4));  // 4 est le facteur d'indentation

            return jsonResponse;
        }
    }

    // Formater la réponse
    public String formatResponse(String analysis) {
        return restTemplate.postForObject(responseFormatterServiceUrl, analysis, String.class);
    }
}
