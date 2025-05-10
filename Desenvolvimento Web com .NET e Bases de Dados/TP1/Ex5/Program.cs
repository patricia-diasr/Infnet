namespace Ex5 {
    internal class Program {
        static void Main(string[] args) {
            DownloadManager manager = new DownloadManager();
            manager.DownloadCompleted += DownloadFinalizado;

            manager.IniciarDownload();
        }
        static void DownloadFinalizado(object sender, EventArgs e) {
            Console.WriteLine("Download concluído com sucesso!");
        }
    }
}
