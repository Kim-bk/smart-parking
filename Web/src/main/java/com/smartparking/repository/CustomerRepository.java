package com.smartparking.repository;

import org.springframework.data.mongodb.repository.MongoRepository;

import com.smartparking.entity.CustomerEntity;


public interface CustomerRepository extends MongoRepository<CustomerEntity, String>{

}
