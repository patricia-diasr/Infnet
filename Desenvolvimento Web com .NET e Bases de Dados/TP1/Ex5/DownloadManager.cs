namespace Ex5 {
    internal class DownloadManager {
        public event EventHandler DownloadCompleted;

        public void IniciarDownload() {
            Console.WriteLine("Realizando download...");
            Thread.Sleep(3000); 
            OnDownloadCompleted();
        }

        public virtual void OnDownloadCompleted() {
            DownloadCompleted?.Invoke(this, EventArgs.Empty);
        }
    }
}
