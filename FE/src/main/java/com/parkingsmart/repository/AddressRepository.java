package com.parkingsmart.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.parkingsmart.entity.AddressEntity;

public interface AddressRepository extends JpaRepository<AddressEntity, Long>{

}
