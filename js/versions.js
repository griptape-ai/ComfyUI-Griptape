export async function getVersion() {
    const response = await fetch("http://127.0.0.1:8188/Griptape/get_version"); // Adjust base URL if needed
    if (!response.ok) {
        console.error("Failed to fetch version:", response.statusText);
        return "Unknown";
    }
    const data = await response.json();
    return data.version;
}
