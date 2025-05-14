import { useEffect, useState } from "react";
import { getFiles, getDownloadLink } from "../api";

export default function Dashboard() {
  const [files, setFiles] = useState([]);
  const [msg, setMsg] = useState("");

  const token = localStorage.getItem("token");

  useEffect(() => {
    getFiles(token)
      .then((res) => setFiles(res.data.files))
      .catch(() => setMsg("Failed to fetch files"));
  }, []);

  const handleDownload = async (id) => {
    try {
      const res = await getDownloadLink(id, token);
      window.open(import.meta.env.VITE_API_URL + res.data["download-link"], "_blank");
    } catch {
      setMsg("Error downloading file");
    }
  };

  return (
    <div>
      <h2>Shared Files</h2>
      <p>{msg}</p>
      <ul>
        {files.map((file) => (
          <li key={file._id}>
            {file.filename}
            <button onClick={() => handleDownload(file._id)}>Download</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
