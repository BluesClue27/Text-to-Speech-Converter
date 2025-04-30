const API_URL = "https://0ma93edu74.execute-api.ap-southeast-1.amazonaws.com/dev/text-to-speech-convertor";

export async function convertTextToSpeech(text, voiceId = "Joanna") {
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text, voiceId }),
        });
        
        if (!response.ok) {
            throw new Error("API response was not OK.");
        }

        const data = await response.json();
        return data.url; // The pre-signed audio URL returned by Lambda
    } catch (error) {
        console.error("Error converting text to speech:", error);
        throw error;
    }
}
