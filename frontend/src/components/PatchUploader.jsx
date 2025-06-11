// frontend/src/components/PatchUploader.jsx
import { useCallback } from "react";
import { useDropzone } from "react-dropzone";

export default function PatchUploader({ onDiff }) {
  const onDrop = useCallback(files => {
    // read the first file as text diff
    const reader = new FileReader();
    reader.onload = () => onDiff(reader.result);
    reader.readAsText(files[0]);
  }, [onDiff]);

  const {getRootProps, getInputProps, isDragActive} = useDropzone({ onDrop });

  return (
    <div
      {...getRootProps()}
      className="border-2 border-dashed rounded p-4 text-center cursor-pointer hover:border-blue-500"
    >
      <input {...getInputProps()} />
      {isDragActive
        ? "Drop your patch file here"
        : "Drag & drop a .diff/.patch file here, or click to select one"}
    </div>
  );
}
