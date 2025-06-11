import { useCallback } from "react";
import { useDropzone } from "react-dropzone";      // docs → :contentReference[oaicite:7]{index=7}
import axios from "axios";

export default function PatchUploader({ onDiff }) {
  const onDrop = useCallback(async (files) => {
    if (!files?.[0]) return;
    const body = new FormData();
    body.append("file", files[0]);
    const { data } = await axios.post("/api/upload", body, {
      headers: { "Content-Type": "multipart/form-data" }
    });
    onDiff(data.diff);
  }, [onDiff]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, accept: { "text/*": [".patch", ".diff"] }
  });

  return (
    <div
      {...getRootProps()}
      className="border-2 border-dashed p-6 text-center rounded cursor-pointer
                 bg-white dark:bg-gray-800 hover:border-blue-500 transition-colors">
      <input {...getInputProps()} />
      {isDragActive
        ? "Drop the patch here…"
        : "Drag & drop a .patch/.diff file, or click to select"}
    </div>
  );
}
