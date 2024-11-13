package com.gcphackaton.api_gatewayms.controller;

import com.gcphackaton.api_gatewayms.model.ArticleRequest;
import com.gcphackaton.api_gatewayms.model.ArticleResponse;
import com.gcphackaton.api_gatewayms.service.ApiGatewayService;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/articles")
public class ArticleController {

    @Autowired
    private ApiGatewayService apiGatewayService;  // Service qui gère la logique de l'API Gateway

    // Route pour traiter un article en POST
    @PostMapping("/process")
    public ResponseEntity<String> processArticle(@RequestBody ArticleRequest articleRequest) {
        try {
            // 1. Récupérer le texte de l'article
            String text = apiGatewayService.retrieveText(articleRequest.getUrl());

            // 2. Analyser la rhétorique de l'article
            JSONObject analysis = apiGatewayService.analyzeRhetoric(text);

            // 3. Formater la réponse
            //String formattedResponse = apiGatewayService.formatResponse(analysis.toString());

            // Créer l'objet ArticleResponse avec les données récupérées
            //ArticleResponse articleResponse = new ArticleResponse(text, analysis.toString(), formattedResponse);

            // Retourner la réponse au frontend
            //return ResponseEntity.ok(articleResponse);
            return ResponseEntity.ok(analysis.toString());

        } catch (Exception e) {
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("message", "Error Leon processing the article");
            return ResponseEntity.status(500).body(errorResponse.toString());
        }
    }
}
