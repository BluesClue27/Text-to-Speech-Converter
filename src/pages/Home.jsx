import React, { useState } from "react";
import { convertTextToSpeech } from "../services/api";
import "../css/Home.css";

function Home() {
  const [text, setText] = useState("");
  const [voice, setVoice] = useState("Joanna");

  const handleConvert = async () => {
    try {
      console.log("Sending text to Lambda: ", text, "Voice: ", voice);
      const audioUrl = await convertTextToSpeech(text, voice);
      const audio = new Audio(audioUrl); 
      audio.play();
    } catch (error){
      console.log("Conversion error: ", error);
      alert("Failed to convert text to speech. Please try again.");
    }
  };

  return (
    <div className="container">
      <h1 className="heading">Text to Speech Converter</h1>
      <div className="card">
        <textarea
          className="textArea"
          placeholder="Type or paste your text here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <div className="controls">
          <select
            className="dropdown"
            value={voice}
            onChange={(e) => setVoice(e.target.value)}
          >
            <option value="Joanna">Joanna (Female, US)</option>
            <option value="Matthew">Matthew (Male, US)</option>
            <option value="Emma">Emma (Female, GB)</option>
            <option value="Brian">Brian (Male, GB)</option>

          </select>
          <button className="button" onClick={handleConvert}>
            Convert to Speech
          </button>
        </div>
      </div>
    </div>
  )
}

export default Home
