
namespace Ex4 {
    internal class TemperatureSensor {

        public event EventHandler<double> TemperatureExceeded;
        public void LerTemperatura(double temperatura) {
            if (temperatura > 100) {
                TemperatureExceeded?.Invoke(this, temperatura);
            }
        }

    }
}
