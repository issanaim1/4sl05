package linkedlists.lockbased;

import java.util.concurrent.locks.ReentrantLock;
import contention.abstractions.AbstractCompositionalIntSet;

public class HandOverHandListBasedSet extends AbstractCompositionalIntSet {

    private Node head;
    private Node tail;
    // Protects entry at head where multiple threads contend simultaneously
    private final ReentrantLock headLock = new ReentrantLock();

    public HandOverHandListBasedSet() {
        head = new Node(Integer.MIN_VALUE);
        tail = new Node(Integer.MAX_VALUE);
        head.next = tail;
    }

    @Override
    public boolean addInt(int item) {
        head.lock();
        Node curr = null;
        Node pred = null;
        try {
            pred = head;
            curr = pred.next;
            curr.lock();
            try {
                while (curr.key < item) {
                    pred.unlock();
                    pred = curr;
                    curr = pred.next;
                    curr.lock();
                }
                if (curr.key == item) {
                    return false;
                } else {
                    Node node = new Node(item);
                    node.next = curr;
                    pred.next = node;
                    return true;
                }
            } finally {
                curr.unlock();
            }
        } finally {
            pred.unlock();
        }
    }

    @Override
    public boolean removeInt(int item) {
        head.lock();
        Node pred = null;
        Node curr = null;
        try {
            try {
                pred = head;
                curr = head.next;
                curr.lock();
                while (curr.key < item) {
                    pred.unlock();
                    pred = curr;
                    curr = pred.next;
                    curr.lock();
                }
                if (curr.key == item) {
                    pred.next = curr.next;
                    return true;
                } else {
                    return false;
                }
            } finally {
                curr.unlock();
            }
        } finally {
            pred.unlock();
        }
    }

    @Override
    public boolean containsInt(int item) {
        head.lock();
        Node pred = null;
        Node curr = null;
        try {
            pred = head;
            curr = head.next;
            curr.lock();
            try {
                while (curr.key < item) {
                    pred.unlock();
                    pred = curr;
                    curr = pred.next;
                    curr.lock();
                }
                if (curr.key == item) {
                    return true;
                } else {
                    return false;
                }
            } finally {
                curr.unlock();
            }
        } finally {
            pred.unlock();
        }
    }

    private class Node {
        public int key;
        public volatile Node next;
        public volatile boolean locked = false;

        Node(int item) {
            key = item;
            next = null;
        }

        public void lock() {
            if (this == head) {
                headLock.lock();
                return;
            }
            // Single-bit lock: safe because pred is locked, so at most 
            // one thread is in this node's trying section at a time.
            while (locked) {}
            locked = true;
        }

        public void unlock() {
            if (this == head) {
                headLock.unlock();
                return;
            }
            locked = false;
        }
    }

    @Override
    public void clear() {
        head = new Node(Integer.MIN_VALUE);
        tail = new Node(Integer.MAX_VALUE);
        head.next = tail;
    }

    @Override
    public int size() {
        int count = 0;
        Node curr = head.next;
        while (curr.key != Integer.MAX_VALUE) {
            curr = curr.next;
            count++;
        }
        return count;
    }
}