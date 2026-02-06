"use client";

import { useState } from "react";
import MicRecorder from "mic-recorder-to-mp3";

const recorder = new MicRecorder({
  bitRate: 128,
});

export default function Home() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [recording, setRecording] = useState(false);

  const BACKEND_URL =
    "https://multilingual-health-ai.onrender.com";

  // -----------------------
  // TEXT MESSAGE
  // -----------------------
  const sendMessage = async () => {
    if (!message) return;

    setLoading(true);
    setReply("");
    setAudioUrl("");

    const res = await fetch(
      `${BACKEND_URL}/chat/text`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
        }),
      }
    );

    const data = await res.json();

    setReply(data.reply_text);

    if (data.audio_url) {
      setAudioUrl(data.audio_url);
      new Audio(data.audio_url).play();
    }

    setLoading(false);
  };

  // -----------------------
  // START RECORDING
  // -----------------------
  const startRecording = () => {
    recorder.start().then(() => {
      setRecording(true);
    });
  };

  // -----------------------
  // STOP + SEND AUDIO
  // -----------------------
  const stopRecording = async () => {
    const [buffer, blob] =
      await recorder.stop().getMp3();

    setRecording(false);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", blob, "voice.mp3");

    const res = await fetch(
      `${BACKEND_URL}/chat/audio`,
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await res.json();

    setReply(data.reply_text);

    if (data.audio_url) {
      setAudioUrl(data.audio_url);
      new Audio(data.audio_url).play();
    }

    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-6">

      <h1 className="text-3xl font-bold mb-6">
        🩺 Multilingual Health AI
      </h1>

      <div className="bg-white shadow-lg rounded-2xl p-6 w-full max-w-xl">

        {/* TEXT INPUT */}
        <input
          type="text"
          placeholder="Describe your symptoms..."
          value={message}
          onChange={(e) =>
            setMessage(e.target.value)
          }
          className="w-full border p-3 rounded-lg mb-4"
        />

        {/* SEND BUTTON */}
        <button
          onClick={sendMessage}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg w-full mb-3"
        >
          {loading ? "Analyzing..." : "Send"}
        </button>

        {/* MIC BUTTON */}
        {!recording ? (
          <button
            onClick={startRecording}
            className="bg-red-600 text-white px-4 py-2 rounded-lg w-full"
          >
            🎤 Start Recording
          </button>
        ) : (
          <button
            onClick={stopRecording}
            className="bg-gray-800 text-white px-4 py-2 rounded-lg w-full"
          >
            ⏹ Stop & Send
          </button>
        )}

        {/* REPLY */}
        {reply && (
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <p className="font-semibold">
              AI Response:
            </p>
            <p>{reply}</p>
          </div>
        )}

        {/* AUDIO PLAYER */}
        {audioUrl && (
          <audio
            controls
            src={audioUrl}
            className="mt-4 w-full"
          />
        )}
      </div>
    </main>
  );
}
