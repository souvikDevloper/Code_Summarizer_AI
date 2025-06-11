import { useState } from "react";
import Editor from "@monaco-editor/react";             // simple usage docs → :contentReference[oaicite:5]{index=5}
import axios from "axios";
import ReactDiffViewer from "react-diff-viewer-continued";  // GitHub → :contentReference[oaicite:6]{index=6}
import PatchUploader from "./components/PatchUploader";

export default function App() {
  const [code, setCode]     = useState("");
  const [result, setResult] = useState("");
  const [preview, setPrev ] = useState(false);

  async function callApi(endpoint) {
    try {
      const { data } = await axios.post(`/api/${endpoint}`, { text: code });
      setResult(data.result);
    } catch (err) {
      setResult("Error: " + err.message);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 p-4 space-y-4">
      <h1 className="text-3xl font-bold text-center text-gray-800 dark:text-gray-100">
        Mini-Codedog
      </h1>

      {/* File drag-and-drop */}
      <PatchUploader onDiff={setCode} />

      {/* Monaco diff editor */}
      <Editor
        height="40vh"
        language="diff"
        value={code}
        onChange={(v)=>setCode(v ?? "")}
        theme="vs-dark"
        options={{ fontSize: 14 }}
      />

      <label className="inline-flex items-center gap-2">
        <input type="checkbox" checked={preview} onChange={e=>setPrev(e.target.checked)} />
        Show diff preview
      </label>

      {preview && (
        <ReactDiffViewer
          oldValue=""
          newValue={code}
          splitView={true}
          className="border rounded"
        />
      )}

      <div className="flex flex-wrap gap-4">
        <button
          onClick={()=>callApi("summarise")}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          Summarise
        </button>
        <button
          onClick={()=>callApi("review")}
          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
          Review
        </button>
      </div>

      <pre className="bg-white dark:bg-gray-800 text-sm p-4 rounded shadow overflow-auto whitespace-pre-wrap">
        {result}
      </pre>
    </div>
  );
}
