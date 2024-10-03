export const Base64ToImage = (base64: string, filename: string) => {
  const parts = base64.split(";base64,")
  const type = parts[0].split(":")[1]
  const data = atob(parts[1])

  const arrayBuffer = new ArrayBuffer(data.length)
  const view = new Uint8Array(arrayBuffer)
  for (let i = 0; i < data.length; i++) {
    view[i] = data.charCodeAt(i) & 0xff
  }

  const blob = new Blob([arrayBuffer], { type })

  const a = document.createElement("a")
  a.href = URL.createObjectURL(blob)
  a.download = filename
  a.click()
}
