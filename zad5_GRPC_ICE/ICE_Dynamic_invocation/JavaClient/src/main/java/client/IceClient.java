package client;
// **********************************************************************
//
// Copyright (c) 2003-2019 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

import Demo.bucketMapHelper;
import Demo.CalcPrx;
import Demo.Transaction;
import com.zeroc.Ice.*;

import java.io.IOException;
import java.lang.Exception;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.CompletableFuture;

public class IceClient 
{
	public static void main(String[] args)
	{
		int status = 0;
		Communicator communicator = null;

		try {
			communicator = Util.initialize(args);

			// 2. Uzyskanie referencji obiektu na podstawie linii w pliku konfiguracyjnym (wówczas aplikacjê nale¿y uruchomiæ z argumentem --Ice.config=config.client)
//			ObjectPrx base1 = communicator.propertyToProxy("Adapter1");
			
			ObjectPrx base1 = communicator.stringToProxy("Adapter1:tcp -h 127.0.0.2 -p 10000 -z : udp -h 127.0.0.2 -p 10000 -z"); //opcja -z w³¹za **mo¿liwoœæ** kompresji
			
			CompletableFuture<Long> cfl = null;
			String line = null;
			java.io.BufferedReader in = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));

			do	{
				try	{
					System.out.println("==> ");
					line = in.readLine();

					switch (line) {
						case "bm" -> {
							OutputStream out = new OutputStream(communicator);
							out.startEncapsulation();
							Map<Integer, int[]> buckets = new HashMap<>();

							buckets.put(1, new int[]{1, 2, 6, 3, 2, 5, 7});
							buckets.put(2, new int[]{11,55,33,88,44,66});
							buckets.put(3, new int[]{131,565,333,848,424,626});
							bucketMapHelper.write(out, buckets);
							out.endEncapsulation();
							byte[] inParams = out.finished();

							com.zeroc.Ice.Object.Ice_invokeResult response = base1.ice_invoke("sortBuckets",  com.zeroc.Ice.OperationMode.Normal, inParams);
							if (!response.returnValue){
								break;
							}

							com.zeroc.Ice.InputStream inStream = new com.zeroc.Ice.InputStream(communicator, response.outParams);
							inStream.startEncapsulation();
							int[] sortedArray = inStream.readIntSeq();
							inStream.endEncapsulation();
							System.out.println("Sorted array of buckets=" + Arrays.toString(sortedArray));
							System.out.println("DONE");
						}
						case "sr" -> {
							OutputStream out = new OutputStream(communicator);
							out.startEncapsulation();
							int[] seq = {1,2,3,4,5,6,7,8,9,10};
							out.writeIntSeq(seq);
							out.endEncapsulation();
							byte[] inParams = out.finished();

							com.zeroc.Ice.Object.Ice_invokeResult response = base1.ice_invoke("sumOfRoots",  com.zeroc.Ice.OperationMode.Normal, inParams);
							if (!response.returnValue){
								break;
							}

							com.zeroc.Ice.InputStream inStream = new com.zeroc.Ice.InputStream(communicator, response.outParams);
							inStream.startEncapsulation();
							double result = inStream.readDouble();
							inStream.endEncapsulation();
							System.out.println("Sum of roots=" + result);
							System.out.println("DONE");
						}
						case "pm" -> {
							OutputStream out = new OutputStream(communicator);
							out.startEncapsulation();
							out.writeString("Bob");
							out.writeFloat(2.0F);
							out.writeString("Adam");
							out.writeInt(15);
							out.endEncapsulation();
							byte[] inParams = out.finished();
							com.zeroc.Ice.Object.Ice_invokeResult response = base1.ice_invoke("payment",  com.zeroc.Ice.OperationMode.Normal, inParams);
							System.out.println("DONE");
						}
						default -> System.out.println("???");
					}
				}
				catch (IOException | TwowayOnlyException ex)
				{
					System.err.println(ex);
				}
			}
			while (!Objects.equals(line, "x"));


		} catch (LocalException e) {
			e.printStackTrace();
			status = 1;
		} catch (Exception e) {
			System.err.println(e.getMessage());
			status = 1;
		}
		if (communicator != null) {
			try {
				communicator.destroy();
			} catch (Exception e) {
				System.err.println(e.getMessage());
				status = 1;
			}
		}
		System.exit(status);
	}

}