import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;

public class Client {
  public static void main(String[] args) throws IOException{
    Socket socket = new Socket();
    socket.connect(new InetSocketAddress("127.0.0.1", 12345));

    socket.getOutputStream().write("hello server".getBytes());
    //this might not work since we also have to flush the data what that means is that we will write it but java might not send it, stores the data in buffer incase extra data is coming so we might have to specifically call flush
    socket.close();
  }
}
