package com.gcphackaton.api_gatewayms.controller;

import com.gcphackaton.api_gatewayms.model.ArticleRequest;
import com.gcphackaton.api_gatewayms.model.ArticleResponse;
import com.gcphackaton.api_gatewayms.service.ApiGatewayService;
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
    public ResponseEntity<ArticleResponse> processArticle(@RequestBody ArticleRequest articleRequest) {
        try {
            // 1. Récupérer le texte de l'article
            String text = apiGatewayService.retrieveText(articleRequest.getUrl());

            // 2. Analyser la rhétorique de l'article
            String analysis = apiGatewayService.analyzeRhetoric(text);

            // 3. Formater la réponse
            String formattedResponse = apiGatewayService.formatResponse(analysis);

            // Créer l'objet ArticleResponse avec les données récupérées
            ArticleResponse articleResponse = new ArticleResponse(text, analysis, formattedResponse);

            // Retourner la réponse au frontend
            return ResponseEntity.ok(articleResponse);

        } catch (Exception e) {
            // En cas d'erreur, retourner un message d'erreur
            return ResponseEntity.status(500).body(new ArticleResponse(null, "Error processing the article", null));
        }
    }
}
