// src/app/ArticleProcessor.js
"use client";
import { useState } from 'react';

function ArticleProcessor() {
    const [url, setUrl] = useState('');
    const [response, setResponse] = useState(null);

    const processArticle = async () => {
        try {
            const res = await fetch("http://localhost:8080/api/articles/process", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ url }),
            });

            if (!res.ok) throw new Error("Erreur lors de l'appel API");

            const data = await res.json();
            setResponse(data);
        } catch (error) {
            console.error("Erreur:", error);
            setResponse({ error: "Impossible de traiter l'article." });
        }
    };

    return (
        <div>
            <h1>Traitement d'Article</h1>
            <input
                type="text"
                placeholder="Entrez l'URL de l'article"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
            />
            <button onClick={processArticle}>Envoyer à l'API Gateway</button>

            {response && (
                <div>
                    <h2>Réponse de l'API:</h2>
                    <pre>{JSON.stringify(response, null, 2)}</pre>
                </div>
            )}
        </div>
    );
}

export default ArticleProcessor;
