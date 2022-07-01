
#ifndef CALC_ICE
#define CALC_ICE

module Demo
{

  exception NoInput {};
  exception EmptySequence {};

  sequence<int> seq;

  dictionary<int, seq> bucketMap;


  struct Transaction
  {
    string seller;
    float moneyAmount;
    string buyer;
    int timestamp;
  }

  interface Calc
  {
    seq sortBuckets(bucketMap buckets);
    double sumOfRoots(seq sq);
    void payment(Transaction tr);
  };

};

#endif
