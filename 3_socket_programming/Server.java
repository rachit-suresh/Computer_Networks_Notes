
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class Server{
  public static void main(String[] args) throws IOException {
    ServerSocket serverSocket = new ServerSocket();
    //server socket is a stream socket and is tcp only
    serverSocket.bind(new InetSocketAddress("127.0.0.1", 12345));
    //as you can see we do not use listen() here since in the api server socket starts listening automatically
    Socket conn = serverSocket.accept();

    Scanner sc = new Scanner(conn.getInputStream());
    //in java u can use either buffer reader or scanner to take input and buffer reader is considered far better than scanner in production, in this above stmt we are trying to get the input stream of the return socket object as tcp gives data as streams
    String data = sc.nextLine();
    System.out.println(data);

    serverSocket.close();
    sc.close();
  }
}